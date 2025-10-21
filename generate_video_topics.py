#!/usr/bin/env python3
"""
Script to generate video topics from Excel file
Processes 5 videos concurrently
"""

import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import logging
import json
import os
import re
from typing import Dict, Any
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API Configuration
API_URL = "http://35.77.64.63:8080/ai/v1/generate-topic"
BEARER_TOKEN = "yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiZ2Fra2VuIiwiaWF0IjoxNTE2MjM5MDIyfQ.uPUicPZRL5Bya61fD0j_ZclC-VsAyueB4aKWWR6mrIs"
MAX_WORKERS = 5  # Number of concurrent requests
REQUEST_TIMEOUT = 300  # Request timeout in seconds (5 minutes)
OUTPUT_DIR = "responses"  # Directory to save response files

def sanitize_filename(filename: str) -> str:
    """
    Convert video name to safe filename

    Args:
        filename: Original video name

    Returns:
        Safe filename for saving
    """
    # Remove file extension if present
    name_without_ext = os.path.splitext(filename)[0]
    # Replace invalid characters with underscore
    safe_name = re.sub(r'[^\w\-_\. ]', '_', name_without_ext)
    # Replace spaces with underscore
    safe_name = safe_name.replace(' ', '_')
    return safe_name

def save_response_to_file(video_name: str, response_data: Dict[str, Any], status: str):
    """
    Save API response to JSON file

    Args:
        video_name: Name of the video
        response_data: Response data from API or error info
        status: Status of the request (success/failed/error)
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Create safe filename
        safe_name = sanitize_filename(video_name)
        output_file = os.path.join(OUTPUT_DIR, f"{safe_name}.json")

        # Prepare data to save
        data_to_save = {
            "video_name": video_name,
            "status": status,
            "data": response_data
        }

        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)

        logger.debug(f"Saved response to: {output_file}")

    except Exception as e:
        logger.error(f"Failed to save response for {video_name}: {str(e)}")

def generate_topic_for_video(row_data: Dict[str, Any], index: int) -> Dict[str, Any]:
    """
    Generate topic for a single video

    Args:
        row_data: Dictionary containing video data from Excel row
        index: Row index for logging

    Returns:
        Dictionary with result status
    """
    try:
        # Extract data from row
        # Adjust column names based on your Excel structure
        video_name = row_data.get('Video Name', '')
        id_video = row_data.get('ID Video', video_name)  # Use Video Name as fallback if no ID column

        # Prepare request payload
        payload = {
            "id_video": str(id_video),
            "object_key": str(video_name)
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }

        logger.info(f"[Row {index + 1}] Processing: {video_name}")

        # Make API request
        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        # Check response
        if response.status_code == 200:
            response_data = response.json()
            logger.info(f"[Row {index + 1}] SUCCESS: {video_name}")

            # Save response to file
            save_response_to_file(video_name, response_data, "success")

            return {
                "index": index,
                "video_name": video_name,
                "status": "success",
                "response": response_data
            }
        else:
            error_data = {
                "status_code": response.status_code,
                "error_message": response.text
            }
            logger.error(f"[Row {index + 1}] FAILED: {video_name} - Status: {response.status_code}")
            logger.error(f"Response: {response.text}")

            # Save error response to file
            save_response_to_file(video_name, error_data, "failed")

            return {
                "index": index,
                "video_name": video_name,
                "status": "failed",
                "error": f"Status {response.status_code}: {response.text}"
            }

    except Exception as e:
        error_data = {
            "error_type": type(e).__name__,
            "error_message": str(e)
        }
        logger.error(f"[Row {index + 1}] ERROR: {str(e)}")

        # Save error to file
        video_name = row_data.get('Video Name', 'Unknown')
        save_response_to_file(video_name, error_data, "error")

        return {
            "index": index,
            "video_name": video_name,
            "status": "error",
            "error": str(e)
        }

def process_excel_file(excel_file_path: str):
    """
    Read Excel file and process videos concurrently

    Args:
        excel_file_path: Path to Excel file
    """
    try:
        # Read Excel file
        logger.info(f"Reading Excel file: {excel_file_path}")
        df = pd.read_excel(excel_file_path)

        logger.info(f"Found {len(df)} videos to process")
        logger.info(f"Columns in Excel: {list(df.columns)}")

        # Check if required column exists
        if 'Video Name' not in df.columns:
            logger.error("Excel file must contain 'Video Name' column")
            logger.info(f"Available columns: {list(df.columns)}")
            return

        # Convert DataFrame to list of dictionaries
        videos = df.to_dict('records')

        # Process videos concurrently
        results = {
            "success": 0,
            "failed": 0,
            "error": 0
        }

        logger.info(f"Starting processing with {MAX_WORKERS} concurrent workers...")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit all tasks
            future_to_video = {
                executor.submit(generate_topic_for_video, video, i): i
                for i, video in enumerate(videos)
            }

            # Process completed tasks
            for future in as_completed(future_to_video):
                result = future.result()
                results[result["status"]] += 1

        # Print summary
        logger.info("\n" + "="*50)
        logger.info("PROCESSING SUMMARY")
        logger.info("="*50)
        logger.info(f"Total videos: {len(videos)}")
        logger.info(f"Successful: {results['success']}")
        logger.info(f"Failed: {results['failed']}")
        logger.info(f"Errors: {results['error']}")
        logger.info(f"Responses saved to: ./{OUTPUT_DIR}/")
        logger.info("="*50)

    except FileNotFoundError:
        logger.error(f"Excel file not found: {excel_file_path}")
    except Exception as e:
        logger.error(f"Error processing Excel file: {str(e)}")
        raise

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python generate_video_topics.py <excel_file_path>")
        print("\nExample:")
        print("  python generate_video_topics.py videos.xlsx")
        print("\nExcel file should contain:")
        print("  - 'Video Name' column (required) - corresponds to object_key")
        print("  - 'ID Video' column (optional) - if not present, Video Name will be used")
        sys.exit(1)

    excel_file = sys.argv[1]
    process_excel_file(excel_file)

if __name__ == "__main__":
    main()
