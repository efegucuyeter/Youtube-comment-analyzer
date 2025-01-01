import customtkinter as ctk
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR, SORT_BY_RECENT
from transformers import pipeline
import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import Counter
import threading

# Helper function to process time field
def process_time_field(time_field):
    """Checks if the comment time field contains 'edited' and separates it."""
    if "(edited)" in time_field:
        return time_field.replace("(edited)", "").strip(), True
    return time_field, False

# Save to Excel
def save_to_excel(selected_columns, comments):
    """Saves the selected columns to an Excel file."""
    filtered_comments = [
        {key: comment[key] for key in selected_columns}
        for comment in comments
    ]
    df = pd.DataFrame(filtered_comments)
    output_file = ctk.filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if output_file:
        df.to_excel(output_file, index=False)
        print(f"Comments saved to {output_file}.")

# Initialize AI models
sentiment_analyzer = pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased", device=0)
classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli", device=0)

# Extended categories
categories = ["Geri Bildirim", "Öneri", "Şikayet", "Spam", "Teşekkür", "Eleştiri", "Sorular", "Genel Tartışma"]

# Batch processing for sentiment analysis
def analyze_sentiments_batch(comments):
    """Performs sentiment analysis on comments in batches."""
    texts = [comment["Text"] for comment in comments]
    sentiments = sentiment_analyzer(texts, batch_size=16)
    for comment, sentiment in zip(comments, sentiments):
        comment["Sentiment"] = sentiment["label"]
        comment["Sentiment_Score"] = sentiment["score"]
    return comments

# Batch processing for topic classification
def classify_topics_batch(comments):
    """Performs topic classification on comments in batches."""
    texts = [comment["Text"] for comment in comments]
    classifications = classifier(texts, categories, batch_size=16)
    for comment, classification in zip(comments, classifications):
        comment["Topic"] = classification["labels"][0]
        comment["Topic_Score"] = classification["scores"][0]
    return comments

# AI processing with batch
def process_comments_with_ai_batch(comments):
    """Processes comments with sentiment analysis and topic classification."""
    comments = analyze_sentiments_batch(comments)
    comments = classify_topics_batch(comments)
    return comments

# Visualization Function
def visualize_results(comments):
    """Visualize sentiment and topic analysis results."""
    if not comments:
        print("No data to visualize!")
        return

    # Create a figure with subplots
    fig, axes = plt.subplots(2, 1, figsize=(10, 12))

    # Sentiment Distribution (Pie Chart)
    sentiments = [comment["Sentiment"] for comment in comments]
    sentiment_counts = Counter(sentiments)
    axes[0].pie(sentiment_counts.values(), labels=sentiment_counts.keys(), autopct="%1.1f%%", colors=['green', 'red', 'blue'])
    axes[0].set_title("Sentiment Distribution")

    # Topic Distribution (Bar Chart)
    topics = [comment["Topic"] for comment in comments]
    topic_counts = Counter(topics)
    axes[1].bar(topic_counts.keys(), topic_counts.values(), color='purple')
    axes[1].set_title("Topic Distribution")
    axes[1].set_xlabel("Topic")
    axes[1].set_ylabel("Count")
    axes[1].tick_params(axis='x', rotation=45)

    # Adjust layout and display the plots
    plt.tight_layout()
    plt.show()

# GUI Application
def display_gui():
    """Displays the GUI for all operations."""
    app = ctk.CTk()
    app.geometry("1000x800")
    app.title("YouTube Comment Downloader")

    # Variables
    video_url_var = ctk.StringVar()
    sort_var = ctk.StringVar(value="1")
    columns_var = {}

    # Status Label
    status_var = ctk.StringVar(value="Ready")
    status_label = ctk.CTkLabel(app, textvariable=status_var, fg_color="gray")
    status_label.pack(pady=5, fill="x")

    def update_status(message):
        """Update the status label with a message."""
        status_var.set(message)

    def fetch_comments():
        """Fetch comments from YouTube based on inputs."""
        def fetch_task():
            update_status("Fetching comments...")
            video_url = video_url_var.get()
            sort_choice = sort_var.get()

            # Determine sorting method
            if sort_choice == "1":
                sort_by = SORT_BY_POPULAR
            elif sort_choice == "2":
                sort_by = SORT_BY_RECENT
            else:
                print("Invalid sorting choice! Defaulting to sort by time.")
                sort_by = SORT_BY_RECENT

            try:
                downloader = YoutubeCommentDownloader()
                comments = downloader.get_comments_from_url(video_url, sort_by=sort_by, language="en")

                comment_list = []
                for idx, comment in enumerate(comments, 1):
                    processed_time, is_edited = process_time_field(comment.get("time", ""))
                    comment_list.append({
                        "Index": idx,
                        "Comment ID": comment.get("cid"),
                        "Text": comment.get("text"),
                        "Time": processed_time,
                        "Edited": str(is_edited).lower(),
                        "Author": comment.get("author"),
                        "Channel": comment.get("channel"),
                        "Votes": comment.get("votes"),
                        "Replies": comment.get("replies"),
                        "Photo URL": comment.get("photo"),
                        "Hearted": str(comment.get("heart", False)).lower(),
                        "Reply": str(comment.get("reply", False)).lower(),
                        "Time Parsed": comment.get("time_parsed")
                    })

                # Populate columns for checkbox selection
                if comment_list:
                    for key in comment_list[0].keys():
                        columns_var[key] = ctk.BooleanVar(value=True)
                        ctk.CTkCheckBox(columns_frame, text=key, variable=columns_var[key]).grid(sticky="w", padx=5, pady=2)

                app.comments = comment_list
                update_status("Comments fetched successfully.")

            except Exception as e:
                update_status(f"An error occurred: {e}")

        threading.Thread(target=fetch_task).start()

    def analyze_comments():
        """Analyze fetched comments with AI models."""
        def analyze_task():
            update_status("Analyzing comments...")
            try:
                if not hasattr(app, 'comments') or not app.comments:
                    update_status("No comments to analyze!")
                    return

                app.comments = process_comments_with_ai_batch(app.comments)

                # Update checkbox for AI-generated fields
                for key in ["Sentiment", "Sentiment_Score", "Topic", "Topic_Score"]:
                    if key not in columns_var:
                        columns_var[key] = ctk.BooleanVar(value=True)
                        ctk.CTkCheckBox(columns_frame, text=key, variable=columns_var[key]).grid(sticky="w", padx=5, pady=2)

                update_status("Comments analyzed successfully.")

            except Exception as e:
                update_status(f"An error occurred during analysis: {e}")

        threading.Thread(target=analyze_task).start()

    def save_comments():
        """Save selected columns to an Excel file."""
        selected_columns = [key for key, var in columns_var.items() if var.get()]
        if not selected_columns:
            update_status("No columns selected!")
            return
        save_to_excel(selected_columns, app.comments)
        update_status("Comments saved to Excel.")

    def visualize_comments():
        """Visualize the analysis results."""
        visualize_results(app.comments)
        update_status("Visualization completed.")

    # Video URL and Sorting Options Frame
    input_frame = ctk.CTkFrame(app)
    input_frame.pack(pady=10, fill="x", padx=10)

    # Video URL Entry
    ctk.CTkLabel(input_frame, text="Enter YouTube Video URL:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    ctk.CTkEntry(input_frame, textvariable=video_url_var, width=300).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Sorting Options
    ctk.CTkLabel(input_frame, text="Sorting Method:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    ctk.CTkRadioButton(input_frame, text="Popularity", variable=sort_var, value="1").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    ctk.CTkRadioButton(input_frame, text="Time", variable=sort_var, value="2").grid(row=3, column=0, padx=5, pady=5, sticky="w")

    # Columns Selection
    columns_frame = ctk.CTkFrame(input_frame)
    columns_frame.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="n")

    # Fetch Comments Button
    ctk.CTkButton(app, text="Fetch Comments", command=fetch_comments).pack(pady=10)

    # Analyze Comments Button
    ctk.CTkButton(app, text="Analyze Comments", command=analyze_comments).pack(pady=10)

    # Save Comments Button
    ctk.CTkButton(app, text="Save to Excel", command=save_comments).pack(pady=10)

    # Visualize Comments Button
    ctk.CTkButton(app, text="Visualize Results", command=visualize_comments).pack(pady=10)

    # Footer Label
    footer_label = ctk.CTkLabel(app, text="Made by Efe Gücüyeter", fg_color="gray")
    footer_label.pack(side="bottom", fill="x", pady=5)

    app.mainloop()

if __name__ == "__main__":
    display_gui()
