# AllRights MVP

## Project Setup Progress

### Day 1:
- Defined MVP scope and outlined tech stack.
- Created accounts for Streamlit, Airtable, and Zapier.

### Day 2:
- Set up development environment.
- Installed necessary libraries: `streamlit`, `requests`, `pandas`, `beautifulsoup4`, `selenium`, `airtable-python-wrapper`, `fpdf`, `opencv-python-headless`.
- Initialized GitHub repository.
- Created initial project structure.

### Day 3:
- **Basic Functionality Tests:**
  - **Streamlit App:** Successfully created and tested a simple Streamlit app.
  - **Web Scraping:** Created and tested a basic web scraper.
  - **Airtable Integration:** Tested Airtable integration with a sample record insertion.

### Day 4:
- **Frontend and Backend Integration:**
  - Created basic `streamlit_app.py` (or `app.py`) in the `frontend` folder.
  - Structured the project with `frontend` and `backend` directories.
  - Added utilities for authentication, deepfake detection, web scraping, and reporting.
  - Implemented user registration, login, content submission, web scraping, and report generation functionalities.

### Day 5:
- **UI Enhancements:**
  - Added a logo to the sidebar and adjusted its size.
  - Improved the layout of the Streamlit app with proper navigation.

### Completed Tasks:
- User Registration/Login:
  - Implemented user registration and login functionalities using Streamlit forms.
  - Integrated Airtable to store user data.
- Content Submission:
  - Designed a form for content URL submission and file uploads.
  - Stored submitted content details in Airtable.
  - Integrated basic deepfake detection using uploaded files.
- Web Scraping:
  - Set up web scraping for images, videos, and audios using BeautifulSoup.
  - Integrated scraping results display in the Streamlit app.
- Reporting:
  - Created a function to generate reports using `fpdf`.
  - Implemented a UI for report generation and download in the Streamlit app.
- Notifications:
  - Set up basic email notifications using Zapier for content submission and analysis results (to be expanded).

### Issues Encountered:
- **Module Import Errors:** Resolved issues related to module imports by adjusting the `sys.path` and project structure.
- **File Path Management:** Ensured that file paths for assets (e.g., logos) are correctly handled across different environments.

## Next Steps:
1. **Refine Functionalities:**
   - Improve deepfake detection accuracy and efficiency.
   - Enhance web scraping capabilities to handle more complex scenarios.
2. **User Testing:**
   - Conduct user testing to gather feedback on the MVP.
   - Iterate based on user feedback and fix any bugs or usability issues.
3. **Documentation:**
   - Document the code and functionalities for easier maintenance and future development.
   - Prepare a demo video or presentation for potential clients and investors.

## How to Run the Project:
1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/allrights.git
   cd allrights
2. **Set up the environment:**
    ```sh
    pip install -r requirements.txt
3. **Run the Streamlit app:**
    ```sh
    streamlit run frontend/app.py

4. **Configure Airtable API:**
    Update the Airtable API keys and base IDs in the backend/authentication/auth.py and other relevant files.

```
AllRights/
├── frontend/
│   ├── app.py
├── backend/
│   ├── authentication/
│   │   └── auth.py
│   ├── deepfake_detection/
│   │   └── detector.py
│   ├── scraping/
│   │   └── scraper.py
│   ├── reporting/
│   │   └── reporter.py
├── assets/
│   │── allrightslogo.png
│   │── allrightslogoblanco.png
├── utils/
│   │   └── airtable.py
├── requirements.txt
├── README.md
```
