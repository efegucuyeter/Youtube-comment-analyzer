# Youtube-comment-analyzer

This project is a YouTube Comment Analysis Application that provides functionalities to fetch, analyze, and visualize comments from a YouTube video.

## Used Technologies

**Language:** Python

**Libraries and Frameworks** customtkinter, youtube-comment-downloader, transformers,pandas, matplotlib, threading, collections.Counter

  
## Used AI

**Sentiment Analysis:** savasy/bert-base-turkish-sentiment-cased

**Topic Classification:** joeddav/xlm-roberta-large-xnli

  
##  Running the Project

1- Clone the Repository

```bash
  git clone https://link-to-project
```

2- Navigate to the project directory:

```bash
  cd my-project
```

3- Install Dependencies

```bash
  pip install -r requirements.txt
```

4- Run the Application

```bash
  python comment_analysis_test.py
```

  
---


## How It Works

1- Fetching Comments

- Enter a YouTube video URL and click "Fetch Comments." 
- The application retrieves comments using a library, sorted either by popularity or time.


2- Analyzing Comments

- Click "Analyze Comments."
- AI models classify each comment by sentiment (positive, negative, neutral) and topic (feedback, suggestions, complaints).

3- Visualizing Results
- Click "Visualize Results" to see:
   - A pie chart for sentiment distribution.
   - A bar chart for topic categorization.

4- Saving Results
- Select specific fields (sentiment, topic) and save them as an Excel file by clicking "Save to Excel."
---


  ## Special Thanks


This project was made possible with the help of the following amazing libraries and their developers:

- **[youtube-comment-downloader](https://github.com/egbertbouman/youtube-comment-downloader)**: A lightweight library for fetching YouTube comments without needing an API. Special thanks to [Egbert Bouman](https://github.com/egbertbouman) for creating this tool.
- **[Transformers](https://github.com/huggingface/transformers)**: A powerful library by [Hugging Face](https://huggingface.co/) for state-of-the-art NLP models. Special thanks to their team for providing accessible AI tools.

---

## Example
1-Enter the Link: Provide the YouTube video link in the designated input field and click the marked button to fetch comments.

![Ekran görüntüsü 2025-01-01 170446](https://github.com/user-attachments/assets/d415be9d-fe19-4954-bd92-5905ce7c590f)

2-Analyze the Comments: Click the "Analyze Comments" button to process the fetched comments for sentiment and topic classification.

![Ekran görüntüsü 2025-01-01 170635](https://github.com/user-attachments/assets/7b4fc9e9-6808-4fbd-99cb-2ed7235c8ac3)


3-Save to Excel: Use the "Save to Excel" button to export the analyzed data into an Excel file.

![Ekran görüntüsü 2025-01-01 170800](https://github.com/user-attachments/assets/485f348e-44b7-4454-a993-bf4578ddabae)


4-Visualize the Data: Click the "Visualize Results" button to generate graphical representations (pie chart and bar chart) of the analysis.

![Ekran görüntüsü 2025-01-01 171311](https://github.com/user-attachments/assets/ca3c26db-144f-4696-b437-fe690c5e12e7)
Visualize Example
![Figure_1](https://github.com/user-attachments/assets/d2798bed-aca0-4ffc-b362-5b387195078c)

  
