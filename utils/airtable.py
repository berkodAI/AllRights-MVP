from airtable import Airtable

def init_airtable(base_id, api_key):
    return Airtable(base_id, 'Content Submissions', api_key)

def add_record(airtable, data):
    airtable.insert(data)

# Test Airtable integration
if __name__ == "__main__":
    base_id = "your_base_id"  # Replace with your base ID
    api_key = "your_api_key"  # Replace with your API key
    airtable = init_airtable(base_id, api_key)
    
    # Example data
    data = {
        "Name": "Test User",
        "Email": "test@example.com",
        "Content URL": "https://www.example.com/content"
    }
    
    add_record(airtable, data)
    print("Record added successfully!")
