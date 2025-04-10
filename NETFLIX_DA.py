#Loading data and Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mtick
from wordcloud import WordCloud
import seaborn as sns
# Part 01 Netflix Content Trend Over the Years

def analyze_netflix_trend(df):

    #Creating copy of the dataframe
    df_copy = df.copy()

    # Creating a Year Added column
    df_copy["year_added"] = df_copy["date_added"].str.split(",").str[1].str.strip()

    # Separate the dataframe on basis of Movies and TV Shows
    movies = df_copy.loc[df_copy["type"] == "Movie"]
    shows = df_copy.loc[df_copy["type"] == "TV Show"]

    # Removing rows where the year_added is empty
    movies = movies[movies["year_added"].notnull()]
    shows = shows[shows["year_added"].notnull()]

    def count_content_yearly(dataframe):
        """  Function which takes a dataframe with year_added column and
        returns a new dataframe with year and no of movies/shows produced in that year  """
        dataframe = dataframe["year_added"]
        dataframe = dataframe[dataframe.str.fullmatch(r"\d{4}")]
        dataframe = dataframe.astype("int")
        dataframe = dataframe.value_counts().sort_index()
        dataframe = dataframe.reset_index()
        dataframe.columns = ["Year", "Count"]

        return dataframe

    movies_year = count_content_yearly(movies)
    shows_year = count_content_yearly(shows)

    # Plotting the data
    fig = plt.figure(figsize=(10, 8))
    axis = fig.add_axes([0.2,0.2,0.7,0.7])
    axis.set_title("Netflix Content Trend Over the Years", fontsize=16, weight="bold")
    axis.set_xlabel("Year", fontsize=14)
    axis.set_ylabel("No of Movies & TV Shows Added", fontsize=14)
    axis.plot(movies_year["Year"], movies_year["Count"], label="Movies", color="mediumblue", ls="dashed", marker=".",
              markerfacecolor="#3066BE", markersize=7)
    axis.plot(shows_year["Year"], shows_year["Count"], label="TV Shows", color="crimson", ls="dashed", marker=".",
              markerfacecolor="#D81E5B", markersize=7)
    axis.legend(title="Content Type", loc=0)
    axis.grid(True, axis="x", color="0.4", dashes=(5, 2))
    axis.set_facecolor("#F5F5F5")
    fig.autofmt_xdate(rotation=25)
    txt = "There was a very notable spike starting from the year 2015\n showing Netflix expansion however there was a dip notable from year 2019"
    props = dict(boxstyle='round', facecolor='white')
    plt.text(2009, 1400, txt, bbox=props)
    plt.show()

# Part 02 Country Wise Netflix Content Production

def analyze_countries_content_production(df):
    df_clean = df.dropna(subset="country").copy()
    df_clean["country"] = df_clean["country"].str.split(",")
    df_clean= df_clean.explode("country")
    df_clean["country"] = df_clean["country"].str.strip()
    df_clean = df_clean.groupby("country").size().reset_index()
    df_clean.columns = ["Country", "Count"]
    df_clean = df_clean.sort_values(by="Count",ascending=True).tail(10)
    fig,axis = plt.subplots(figsize=(10,8))
    axis.set_title("Country-Wise Netflix Content Production", fontsize=16, weight="bold")
    axis.set_xlabel("No of Movies and TV Shows Produced", fontsize=14)
    axis.set_ylabel("Countries", fontsize=14)
    norm = plt.Normalize(df_clean["Count"].min(), df_clean["Count"].max())
    colors = mpl.colormaps["turbo"](norm(df_clean["Count"]))
    bars = axis.barh(df_clean["Country"],df_clean["Count"],color=colors,edgecolor="#1A1F16")
    axis.set_facecolor("#F5F5F5")
    def formatter(value,_):
        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f}M"
        elif value >= 1_000:
            return f"{value/1_000:.1f}K"
        else:
            return f"{value:.0f}"
    axis.xaxis.set_major_formatter(mtick.FuncFormatter(formatter))
    for bar in bars:
        w = bar.get_width()
        y = bar.get_y() + bar.get_height()/2
        x = w - (w*0.1)
        axis.text(x,y,str(w),va="center",ha="right",fontsize=10,color="#FFFFFF")

    plt.show()

# Part 03 Analyzing what kind of content Netflix mostly adds

def analyze_target_audience_analysis(df):
    plt.rcParams['font.family'] = 'Segoe UI Emoji'
    #Remove any rows in ratings column with NaN values
    df_copy = df.dropna(subset=["rating"]).copy()
    #Removing any odd values in ratings columns, i.e "66 min" .
    df_copy = df_copy[~df_copy["rating"].str.contains(r"^\d+\s*min$")]
    #Assigning general category to ratings like Rating PG comes under Parental Guidance Suggested general rating
    general_category = {"TV-Y": "General Audience (All Ages)", "TV-Y7": "General Audience (All Ages)",
                        "TV-Y7-FV": "General Audience (All Ages)", "TV-G": "General Audience (All Ages)",
                        "G": "General Audience (All Ages)", "PG": "Parental Guidance Suggested",
                        "PG-13": "Parental Guidance Suggested", "TV-PG": "Parental Guidance Suggested",
                        "TV-14": "Restricted / Mature (17+)", "R": "Restricted / Mature (17+)",
                        "TV-MA": "Restricted / Mature (17+)", "NC-17": "Restricted / Mature (17+)",
                        "NR": "Unrated / Not Classified", "UR": "Unrated / Not Classified"}
    df_copy["general_rating"] = df_copy["rating"].map(general_category).fillna("Others")
    #Grouping the dataframe by general rating
    df_copy = df_copy.groupby("general_rating").size()
    df_copy = df_copy.reset_index()
    df_copy.columns = ["Ratings", "Count"]
    #Plotting
    figure, axis = plt.subplots(figsize=(10, 8))

    explode = [0.05 if val == df_copy["Count"].max() else 0 for val in df_copy["Count"]]
    colors = ("#648FFF", "#785EF0", "#DC267F", "#FE6100")
    axis.set_title("Majority of Netflix Content Targets Mature Audiences",fontdict=dict({"fontsize":"18","fontweight":"bold"}))
    axis.pie(df_copy["Count"], labels=df_copy["Ratings"], autopct='%1.1f%%', colors=colors, pctdistance=0.85, explode=explode)

    circ = plt.Circle((0, 0), 0.7, fc="white", edgecolor="white")
    axis.add_artist(circ)
    axis.legend(title="Ratings",loc=0,bbox_to_anchor=(0, 0.5))
    text = "Netflix generally contains content which is Mature(17+).\nThere is also an interesting insight that Kids Content is slightly more than the content targeted to General Audience"
    axis.text(0, -1.3, text,
             ha='center', fontsize=11, color='gray',bbox=dict(facecolor='none', edgecolor='gray', pad=10.0))
    axis.text(0,0.0,"Audience Category",ha="center",va="center")
    plt.show()

    """Some Insights :-  NetFlix generally contains content which is mature.There is also an interesting insight that
    Kids Content is slightly more than the content targeted to General Audience"""
    
# Part 04 Analyzing Top Genres Found in Netflix

def analyze_netflix_genres_over_years(df):
    df_copy = df.copy()
    #Adding a Year Added column
    df_copy["year_added"] = df_copy["date_added"].str.split(",").str[1].str.strip()
    #Dropping NaN Values
    df_copy = df_copy.dropna(subset=["year_added"])
    df_copy = df_copy.rename(columns={"listed_in": "Genres"})
    df_copy["Genres"] = df_copy["Genres"].str.split(",")
    df_copy = df_copy.explode("Genres")
    df_copy["Genres"] = df_copy["Genres"].str.strip()
    #Getting Top 7 Genres that are widely added
    top_genres = df_copy["Genres"].value_counts().head(7).index
    df_copy["Theme"] = np.where(df_copy["Genres"].isin(top_genres), df_copy["Genres"], "Others")
    df_copy = df_copy.groupby(["year_added", "Theme"]).size()
    df_copy = df_copy.reset_index()
    df_copy.columns = ["Year", "Theme", "Count"]
    pivot = df_copy.pivot_table(index="Year", columns="Theme", values="Count", aggfunc="sum").fillna(0)
    pivot = pivot.drop(columns=["Others"])
    pivot = pivot[pivot.sum().sort_values(ascending=False).index]
    colors = ["#A7BED3", "#C6E2E9", "#F1FFC4", "#FFCAAF", "#FFC759", "#FF7B9C", "#DBCBD8"]
    fig, ax = plt.subplots(figsize=(10, 8))

    x = pivot.index
    y = [pivot[col] for col in pivot.columns]
    ax.stackplot(x, y, labels=pivot.columns, colors=colors, edgecolor="black", linewidth=0.5)
    ax.legend(loc=0, title="Genres")
    ax.set_facecolor("#EBEBEB")
    props = dict(boxstyle='round,pad=1', facecolor='white')
    ax.text(2,300,"Note : Since there was large collections of Genres,\n displayed only top 7 Genres", fontsize=10,
                 alpha=0.8,bbox=props,ha="center")
    ax.set_title("Netflix's Content Focus Over the Years: Top Genres", fontsize=18)
    ax.set_xlabel("Year",fontsize=14)
    ax.set_ylabel("No of Genres added",fontsize=14)
    ax.set_axisbelow(True)
    ax.grid(True, axis="x", color="0.6", dashes=(2, 4))
    plt.show()
def analyze_frequent_netflix_collaborators(df):
    df_copy = df.copy()
    df_copy["cast"] = df_copy["cast"].str.split(",")
    df_copy = df_copy.explode("cast")
    df_copy["cast"] = df_copy["cast"].str.strip()
    df_copy = df_copy.dropna(subset=["cast"])
    df_copy = df_copy.groupby("cast").size().reset_index()
    df_copy.columns = ["Actor Name", "Count"]
    df_copy = df_copy.sort_values(by="Count", ascending=False).reset_index().head(50)
    actor_dictionary = dict(zip(df_copy['Actor Name'], df_copy['Count']))

    wordcloud = WordCloud(width=1000,height=600,background_color="white",colormap="tab10").generate_from_frequencies(actor_dictionary)

    plt.figure(figsize=(12,8))
    plt.imshow(wordcloud,interpolation="bilinear")
    plt.axis("off")
    plt.title("Most Frequent Collaborators (Actors)",fontsize=20,pad=20)
    plt.show()

def analyze_netflix_content_freshness(df):
    df_copy = df.copy()
    df_copy["date_added"] = df["date_added"].str.strip()
    df_copy["date_added"] = pd.to_datetime(df_copy["date_added"],errors="coerce",format="mixed")
    df_copy = df_copy.dropna(subset = ["date_added"])
    df_copy["year_added"] = df_copy["date_added"].dt.year
    df_copy["year_added"] = df_copy["year_added"].astype("int")
    df_copy = df_copy.groupby(["year_added","type"]).size().reset_index()
    df_copy.columns = ["Year","Type","Count"]
    pivot_table = df_copy.pivot_table(index="Year",columns="Type",values="Count").fillna(0)

    figure,axis = plt.subplots(figsize=(10,8))
    axis.set_title("Netflix Content Freshness",fontsize=20,pad=20,fontweight="bold")
    axis.set_xlabel("Type",fontsize=12)
    axis.set_ylabel("Year", fontsize=12)
    heatmap = sns.heatmap(pivot_table,annot=True,fmt=".0f",linewidth="1",cmap="plasma",linecolor="white",annot_kws={"size":10},ax=axis)
    plt.show()
if __name__ == "__main__":
    main_df = pd.read_csv("data/netflix_data.csv")
    analyze_netflix_trend(main_df)
    analyze_countries_content_production(main_df)
    analyze_target_audience_analysis(main_df)
    analyze_netflix_genres_over_years(main_df)
    analyze_frequent_netflix_collaborators(main_df)
    analyze_netflix_content_freshness(main_df)