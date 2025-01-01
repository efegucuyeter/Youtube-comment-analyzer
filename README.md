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



## Example

  
