# Screenshot Archiver & Dashboard

This project automates the process of archiving screenshots on macOS and provides a web-based dashboard to view and manage the archived files.

## Project Overview

The system is composed of two main parts:
1.  **Archival Script (`organize_screenshots.sh`):** A shell script that runs on a schedule (via a CRON job) to find screenshots older than one day across the Desktop, Downloads, and Documents folders and move them to a central archive.
2.  **Web Dashboard (`app.py`):** A local web application built with Python and Flask that provides a user interface to interact with the screenshot archive.

---

## Dashboard Implementation Walkthrough

The dashboard was built to provide a simple and effective way to visualize the output of our CRON job.

### 1. Backend Development (Flask)

The backend is a single Python script (`app.py`) powered by the **Flask** web framework.

-   **File & Stat Processing:** The main logic reads the contents of the `~/Documents/old files` directory. It calculates key statistics like the total number of files and the total disk space used. For the activity chart, it processes the modification date of each file, grouping them by day to create a time-series dataset.
-   **Routing:**
    -   `@app.route('/')`: The main endpoint that renders the dashboard. It fetches all the stats and file data and passes it to the HTML template.
    -   `@app.route('/run-script')`: This endpoint is triggered by the "Run Now" button. It uses Python's `subprocess` module to execute the `organize_screenshots.sh` script manually.
    -   `@app.route('/view/<filename>')`: A dynamic route that serves the actual image files, allowing users to click on a thumbnail in the dashboard and see the full-sized screenshot.

### 2. Frontend Development (HTML & Chart.js)

The frontend is a single HTML file (`templates/dashboard.html`) that is rendered by Flask.

-   **Structure & Styling:** The page uses semantic HTML and includes modern, minimal CSS for a clean user interface. The layout is organized into "cards" for different sections like stats, the chart, and the file grid.
-   **Dynamic Data:** The template uses Jinja2 syntax (e.g., `{{ file_count }}`) to display the data passed from the Flask backend.
-   **Interactive Chart:** The line chart is rendered using the **Chart.js** library. We added a `<canvas>` element to the HTML and then used a small JavaScript block to initialize the chart, feeding it the time-series data (labels and counts) that was processed by our Python script.

---

## Technologies Used

-   **Backend:** Python 3, Flask
-   **Frontend:** HTML5, CSS3, JavaScript
-   **Charting:** Chart.js
-   **Automation:** Shell Scripting, CRON
-   **Version Control:** Git, GitHub

---

## Code Snippet Breakdown

### `app.py` - Data Analysis for Chart

This function is the core of the dashboard's data processing. It analyzes the files in the archive to generate all the necessary statistics for the frontend.

```python
def get_archive_stats():
    """Calculates statistics about the archive directory."""
    files = [f for f in os.listdir(ARCHIVE_DIR) if f.lower().endswith('.png')]
    file_count = len(files)
    total_size = sum(os.path.getsize(os.path.join(ARCHIVE_DIR, f)) for f in files)
    
    # Process data for the chart by grouping files by modification day
    activity_by_day = defaultdict(int)
    for f in files:
        mod_time = os.path.getmtime(os.path.join(ARCHIVE_DIR, f))
        day = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
        activity_by_day[day] += 1
        
    # Sort the dates and prepare data for JSON serialization to the template
    sorted_days = sorted(activity_by_day.keys())
    chart_labels = json.dumps(sorted_days)
    chart_data = json.dumps([activity_by_day[day] for day in sorted_days])
    
    # Calculate average
    num_days = len(activity_by_day)
    average_per_day = round(file_count / num_days if num_days > 0 else 0, 2)
    
    return file_count, total_size, files, chart_labels, chart_data, average_per_day
```

### `dashboard.html` - Chart.js Initialization

This JavaScript snippet, located at the bottom of the HTML file, takes the data prepared by Flask and uses it to render the line chart.

```javascript
<script>
    const ctx = document.getElementById('activityChart').getContext('2d');
    const activityChart = new Chart(ctx, {
        type: 'line',
        data: {
            // The `|safe` filter is used to render the JSON string from Flask
            labels: {{ chart_labels|safe }},
            datasets: [{
                label: 'Screenshots Archived',
                data: {{ chart_data|safe }},
                backgroundColor: 'rgba(24, 119, 242, 0.2)',
                borderColor: 'rgba(24, 119, 242, 1)',
                borderWidth: 2,
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
</script>
```

---

## 🤖 LLM System Prompt

This prompt can be used to guide a sufficiently capable Large Language Model to recreate this project.

> You are an expert software engineering assistant. Your goal is to create a local web dashboard to monitor a file archival process on a user's macOS computer.
>
> **Project Requirements:**
> 1.  **Technology Stack:** Use Python 3 with the Flask web framework for the backend. The frontend should be a single HTML file with embedded CSS and JavaScript.
> 2.  **Dashboard Features:**
>     *   **Statistics:** Display the total number of files and the total size of files in the archive directory, which is located at `~/Documents/old files`.
>     *   **Activity Chart:** Create a line chart that shows the number of files archived per day. You must derive this data by analyzing the modification timestamps of the files in the archive directory. Use the Chart.js library for this, loaded from a CDN.
>     *   **File Viewer:** Display the archived screenshots in a responsive grid. Each image should be a thumbnail that links to the full-size version.
>     *   **Manual Trigger:** Include a button that, when clicked, executes an external shell script located at `~/screenshot_archives/organize_screenshots.sh`.
> 3.  **Implementation Details:**
>     *   The Python script should be a single `app.py` file.
>     *   The HTML should be in a `templates/dashboard.html` file.
>     *   The application should run on port 5001.
>     *   The design should be clean and modern, using a card-based layout.
>     *   Provide clear, final instructions on how to run the application.
>
> Execute this plan step-by-step.