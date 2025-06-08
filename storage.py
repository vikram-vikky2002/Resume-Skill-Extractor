import json
import os
from datetime import datetime
import uuid

class ResumeStorage:
    """
    Class to handle storage and retrieval of resume parsing results.
    """
    def __init__(self, storage_file='results.json'):
        """
        Initialize the storage system.
        
        Args:
            storage_file (str): Path to the JSON storage file
        """
        self.storage_file = storage_file
        
        # Create storage file if it doesn't exist
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump([], f)
    
    def save_result(self, data, filename, summary, category):
        """
        Save a parsed resume result to storage with summary and category.
        
        Args:
            data (dict): Parsed resume data
            filename (str): Name of the uploaded file
            summary (str): Generated summary
            category (str): Resume category
            
        Returns:
            str: ID of the saved result
        """
        try:
            # Load existing results
            with open(self.storage_file, 'r') as f:
                results = json.load(f)
                
            # Generate a unique ID and ensure it's unique
            result_id = str(uuid.uuid4())
            while any(r['id'] == result_id for r in results):
                result_id = str(uuid.uuid4())
                
            # Add new result with timestamp and unique ID
            result_data = {
                'id': result_id,
                'filename': filename,
                'timestamp': datetime.now().isoformat(),
                'data': data,
                'category': category,  # Save the category
                'remarks': '',    # Initialize empty remarks
                'summary': summary    # Save the summary
            }
            
            # Add to results list
            results.append(result_data)
            
            # Save updated results
            with open(self.storage_file, 'w') as f:
                json.dump(results, f, indent=4)
            return result_id  # Return the generated ID
        except Exception as e:
            print(f"Error saving result: {str(e)}")
            return None
    
    def load_all_results(self):
        """
        Load all stored resume parsing results.
        
        Returns:
            list: List of all stored results
        """
        try:
            with open(self.storage_file, 'r') as f:
                results = json.load(f)
            return results
        except Exception as e:
            print(f"Error loading results: {str(e)}")
            return []
    
    def get_result_by_id(self, result_id):
        """
        Get a specific result by its ID.
        
        Args:
            result_id (str): ID of the result to retrieve
            
        Returns:
            dict: The requested result or None if not found
        """
        results = self.load_all_results()
        for result in results:
            if result['id'] == result_id:
                return result
        return None

    def update_category(self, result_id, category):
        """
        Update category for a specific result. Handles both single and multiple categories.
        
        Args:
            result_id (str): ID of the result to update
            category (str or list): New category or list of categories
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            with open(self.storage_file, 'r') as f:
                results = json.load(f)
            
            for result in results:
                if result['id'] == result_id:
                    # If category is a list, store it as a list
                    if isinstance(category, list):
                        result['category'] = category
                    else:
                        # If result already has a list of categories, append the new one
                        if isinstance(result['category'], list):
                            if category not in result['category']:
                                result['category'].append(category)
                        else:
                            # If result has a single category, convert to list and add new category
                            if result['category'] and result['category'] != category:
                                result['category'] = [result['category'], category]
                            else:
                                result['category'] = category
                    break
            
            with open(self.storage_file, 'w') as f:
                json.dump(results, f, indent=4)
            return True
        except Exception as e:
            print(f"Error updating category: {str(e)}")
            return False

    def update_summary(self, result_id, summary):
        """
        Update summary for a specific result.
        
        Args:
            result_id (str): ID of the result to update
            summary (dict): Summary information
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            with open(self.storage_file, 'r') as f:
                results = json.load(f)
            
            for result in results:
                if result['id'] == result_id:
                    result['summary'] = summary
                    break
            
            with open(self.storage_file, 'w') as f:
                json.dump(results, f, indent=4)
            return True
        except Exception as e:
            print(f"Error updating summary: {str(e)}")
            return False
            
    def update_remarks(self, result_id, remarks):
        """
        Update remarks for a specific result.
        
        Args:
            result_id (str): ID of the result to update
            remarks (str): New remarks text
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            with open(self.storage_file, 'r') as f:
                results = json.load(f)
            
            for result in results:
                if result['id'] == result_id:
                    result['remarks'] = remarks
                    break
            
            with open(self.storage_file, 'w') as f:
                json.dump(results, f, indent=4)
            return True
        except Exception as e:
            print(f"Error updating remarks: {str(e)}")
            return False

    def search_results(self, query="", category_filter=None):
        """
        Search through stored results with optional category filtering.
        
        Args:
            query (str): Search term to filter results
            category_filter (str): Category to filter by
            
        Returns:
            list: List of matching results
        """
        try:
            with open(self.storage_file, 'r') as f:
                results = json.load(f)
            
            matching_results = []
            
            for result in results:
                # Check category filter first if provided
                if category_filter and result.get('category') != category_filter:
                    continue
                    
                # If no query, add to results
                if not query:
                    matching_results.append(result)
                    continue
                    
                # Search in filename, name, email, phone, and skills
                search_text = f"{result['filename']} {result['data'].get('name', '')} {result['data'].get('email', '')} {result['data'].get('phone', '')} {' '.join(result['data'].get('skills', []))}".lower()
                if query.lower() in search_text:
                    matching_results.append(result)
            
            return matching_results
        except Exception as e:
            print(f"Error searching results: {str(e)}")
            return []

    def delete_result(self, result_id):
        """
        Delete a specific result by its ID.
        
        Args:
            result_id (str): ID of the result to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            results = self.load_all_results()
            results = [r for r in results if r['id'] != result_id]
            
            with open(self.storage_file, 'w') as f:
                json.dump(results, f, indent=4)
            return True
        except Exception as e:
            print(f"Error deleting result: {str(e)}")
            return False
