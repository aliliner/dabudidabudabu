import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry_convert as pc
import requests

df = pd.read_csv(r'C:\Users\lizzie\Desktop\HAC_2.csv')
population = pd.read_csv(r'C:\Users\lizzie\Desktop\population.csv')
df_w = pd.read_csv(r'C:\Users\lizzie\Desktop\WAl.csv')

with st.echo(code_location='below'):
    cont_names = {"AF": "Africa",
                  "AS": "Asia",
                  "EU": "Europe",
                  "NA": "North America",
                  "OC": "Oceania",
                  "SA": "South America"}

    df["Sum_PerCapita"] = df["Beer_PerCapita"] + df["Spirit_PerCapita"] + df["Wine_PerCapita"]


    def change(ccon_name):
        return (pc.country_name_to_country_alpha3(cn_name=ccon_name))


    def change_to_alpha2(c_name):
        return (pc.country_name_to_country_alpha2(cn_name=c_name))


    def change_code_to_continent(code):
        return (pc.country_alpha2_to_continent_code(code))


    df['iso_alpha'] = df.apply(lambda row: change(row['Country']), axis=1)
    df['code_2'] = df.apply(lambda row: change_to_alpha2(row['Country']), axis=1)
    df["Continent"] = df.apply(lambda row: change_code_to_continent(row['code_2']), axis=1)
    df["Continent"] = df["Continent"].map(cont_names)
    country_list = sorted(df["Country"].tolist())

    df_p = pd.merge(df, population, left_on="iso_alpha", right_on='CountryCode',
                    how="left", sort=False)
    df_p['TotalConsumption_mln'] = df_p["Sum_PerCapita"].astype(float) * df_p["Y2016"].astype(float) / 10 ** 6

    st.title("Sobriety is not in our VODKAbulary")
    st.markdown("""
     Wine, rum, whiskey, cognac, brandy, vodka, beer, cider, gin, liqueurs... This list seems endless. Every person on the planet has at least heard about alcohol, which can be considered one of the most dangerous drugs (David Nutt, 2020). 

     While reading my work, do not forget that alcohol is bad for your health!   
        """)

    st.markdown("""
     Here you will find out a little more about alcohol, about alcohol consumption in different regions and whether this consumption brings happiness.
        """)

    st.subheader("Alcohol servings per capita")

    st.markdown("""
     Let's start by exploring the world map, where you can see alcohol consumption per capita in different countries. 
     I would like to draw your attention to the fact that the graph is **interactive**: you can **adjust** the scale 
     and **select** the parts of our planet which are interesting for you, and also find out specific values when you point at the country. 
     Turn on the **full-screen graphics mode** of the map to get a better look!
      """)

    al_map = px.choropleth(df, color="Sum_PerCapita",
                           locations="iso_alpha",
                           hover_name="Country",
                           height=450,
                           color_continuous_scale="Viridis",
                           title="Alcohol servings per capita in the world",
                           labels={"Sum_PerCapita": "servings per capita"})
    al_map.update_layout(
        title_font=dict(size=20),
        legend_font=dict(size=15),
        height=525,
        width=750
    )
    st.plotly_chart(al_map)

    st.markdown("""
     This interactive map is a confirmation that alcohol consumption in the world is very uneven. It depends on a large number 
     of factors, including religion, laws, culture and other reasons. But that's not the point now.
      """)

    st.markdown("""
    As I noticed at the beginning, alcohol can be very different, from light cider to brutal absinthe. 
    Let's look at the relative distribution of alcohol consumption between countries. Let's limit ourselves to the three 
    most popular categories: wine, beer and spirit.
    """)

    st.subheader("Popularity of wine, beer and spirit among countries")

    st.markdown("""
    The popularity of a particular type of alcohol in each country was influenced by climatic conditions and cultural characteristics, as I said earlier. Residents of each country are unique in their preferences about the main three categories of alcohol - wine, beer and alcohol. I decided to draw on one graph the consumption per capita of beer, wine and alcohol and standardize. On the graph, the size of the balls corresponds to the population of the country, thus you can see how the population of our planet is distributed between these three categories of alcohol.
    """)

    df_p['Population'] = df_p['Y2016'].astype(float)
    tr_w = px.scatter_ternary(df_p, a="Beer_PerCapita", b="Spirit_PerCapita", c="Wine_PerCapita",
                              hover_name="Country",
                              size="Population",
                              color_discrete_sequence=["teal"],
                              size_max=40,
                              opacity=0.8,
                              title="The ratio of wine, beer and spirit consumption per capita among countries",
                              labels={"Beer_PerCapita": "Beer",
                                      "Spirit_PerCapita": "Spirit",
                                      "Wine_PerCapita": "Wine"}
                              )
    tr_w.update_layout(
        title_font=dict(size=20),
        font_size=15,
        height=600,
    )
    st.plotly_chart(tr_w)

    st.markdown("""
    As in the previous graph, you can study it in more detail if you **hover the mouse**.

    It should be noted that so far there is a strong bias towards beer and spirit, but relatively more wine is consumed by European countries such as Italy and France.
    """)

    st.write("""
        Let's look at the distribution of preferences by region. There are interactive graphs which allows you to **select** or **exclude** the region you want (just click on the legend), so there is no point in making a switch in case of continents. 
        """)
    level = st.radio(
        "Choose the level of comparison",
        ("Continents", "Countries"))

    if level == "Continents":
        st.write(
            "In this section I give you the opportunity to compare several continents. You can choose regions in legend.")

        tr_w_col = px.scatter_ternary(df_p, a="Beer_PerCapita", b="Spirit_PerCapita", c="Wine_PerCapita",
                                      hover_name="Country",
                                      color="Continent",
                                      size="Population",
                                      size_max=40,
                                      opacity=0.9,
                                      labels={"Beer_PerCapita": "Beer",
                                              "Spirit_PerCapita": "Spirit",
                                              "Wine_PerCapita": "Wine"},
                                      color_discrete_sequence=px.colors.qualitative.Prism
                                      )
        tr_w_col.update_layout(
            title_font=dict(size=20),
            font_size=15,
            height=600,
        )
        st.plotly_chart(tr_w_col)

    else:
        st.write(
            """In this section I give you the opportunity to compare several countries. You can choose as many countries as you want. On the graph, the size of the country reflects its population. """)

        ch_coun = st.multiselect("Select countries", country_list, default=["Italy", "Peru", "Brazil"])
        tr_w_con = px.scatter_ternary(df_p[df_p["Country"].isin(ch_coun)], a="Beer_PerCapita",
                                      b="Spirit_PerCapita", c="Wine_PerCapita",
                                      hover_name="Country",
                                      color="Country",
                                      size="Population",
                                      opacity=0.9,
                                      size_max=40,
                                      labels={"Beer_PerCapita": "Beer",
                                              "Spirit_PerCapita": "Spirit",
                                              "Wine_PerCapita": "Wine"},
                                      color_discrete_sequence=px.colors.qualitative.Prism
                                      )
        tr_w_con.update_layout(
            title_font=dict(size=20),
            font_size=15,
            height=600,
        )
        st.plotly_chart(tr_w_con)

    st.header("What happens to absolute values?")

    st.markdown("""
    After we have discussed the relative values, it is enticing to look at the absolute values of alcohol consumption. The 
    results are presented in the form of an interactive treemap. Click to enlarge or find out more information. If you **click** on the region, you can find out even more (try it!).
    """)

    df_tree = df_p[["Country", "Region", "CountryCode", "TotalConsumption_mln"]]
    al_tree = px.treemap(df_tree, path=[px.Constant("World"), "Region", "Country"],
                         values="TotalConsumption_mln",
                         hover_data=["Country"],
                         title="Alcohol consumption in the world",
                         color_discrete_sequence=px.colors.sequential.Viridis
                         )
    al_tree.update_layout(
        title_font=dict(size=20),
        font=dict(size=15),
        height=600
    )
    st.plotly_chart(al_tree)

    st.markdown("""
    In this treemap, we see the distribution of total alcohol consumption between regions of the world. Please note that the number of people plays a significant role when comparing total alcohol consumption.
    """)

    st.markdown("""
    Make sure you tried clicking on the graph!
    """)

    st.header("Happiness and alcohol")

    st.markdown("""
    Does drinking alcohol make people happier? And in a global perspective, does a high level of alcohol consumption mean a higher happiness index in the country?
    """)

    st.markdown("""
    In the graph below, I am trying to identify the relationship between the level of happiness in the country and the amount of alcohol consumed per capita.
    """)

    df_wb = df.loc[df["Hemisphere"].astype(str).isin(["north", "south"])]
    plot_1 = px.scatter(data_frame=df_wb,
                        x="Sum_PerCapita",
                        y="HappinessScore",
                        hover_name="Country",
                        color="Hemisphere",
                        trendline="ols",
                        title="Connection between the Happiness score and Alcohol per capita",
                        labels={"HappinessScore": "Happiness Score",
                                "Sum_PerCapita": "Alcohol servings per capita (per year)"},
                        color_discrete_sequence=["yellowgreen", "teal"])
    plot_1.update_layout(
        title_font=dict(size=20),
        legend_font=dict(size=15),
        height=700,
        title_text="Connection between the happiness score and alcohol per capita"
    )
    st.plotly_chart(plot_1)

    st.markdown("""
    In both hemispheres, we can observe a weak but positive relationship between the amount of alcohol consumed and the level of happiness. However, we remember that a connection does not mean a causation, so do not rush to drink every day!
    """)

    st.subheader("Let 's drop down to the country level")

    st.markdown("""
    In this section I want to give you the opportunity to view information on the country that you choose
    """)

    option = st.selectbox(
        "Select a country", country_list, index=52)

    country = option
    c_beer = df.loc[df["Country"] == country]["Beer_PerCapita"].values[0]
    c_spirit = df.loc[df["Country"] == country]["Spirit_PerCapita"].values[0]
    c_wine = df.loc[df["Country"] == country]["Wine_PerCapita"].values[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Beer Per Capita", c_beer)
    col2.metric("Spirit Per Capita", c_spirit)
    col3.metric("Wine Per Capita", c_wine)

    st.markdown("""
    The alcohol preferences are shown more indicatively on the basis of triangular normalized beer-wine-alcohol coordinates. Let's mark the selected country:
    """)

    tr_con = px.scatter_ternary(df.loc[df["Country"] == country], a="Beer_PerCapita",
                                b="Spirit_PerCapita", c="Wine_PerCapita",
                                hover_name="Country",
                                opacity=0.8,
                                size=[8],
                                title="Map of alcohol preferences of the selected country",
                                labels={"Beer_PerCapita": "Beer",
                                        "Spirit_PerCapita": "Spirit",
                                        "Wine_PerCapita": "Wine"},
                                color_discrete_sequence=["teal"]
                                )
    tr_con.update_layout(
        title_font=dict(size=20),
        title_x=0.5,
        font_size=15,
        height=500,
    )
    st.plotly_chart(tr_con)

    st.markdown("""
    For a better understanding of the country, I display other metrics:
    """)

    c_happ = df.loc[df["Country"] == country]["HappinessScore"].values[0]
    c_hdi = df.loc[df["Country"] == country]["HDI"].values[0]
    c_gdp = df.loc[df["Country"] == country]["GDP_PerCapita"].values[0]

    col11, col12, col14, col15 = st.columns(4)

    with col11:
        st.write(" ")
    col12.metric("HDI (out of 1000)", c_hdi)
    col14.metric("Happiness Score (out of 9)", c_happ)
    with col15:
        st.write(" ")

    st.subheader("Animation at the end")

    st.markdown("""
    In this section, you can select the top countries by alcohol consumption and see how the structure of this top has changed over the course of about 20 years.
    """)

    n_top = st.number_input(label="Choose X to look at top-X countries by alcohol consumption:",
                            min_value=1,
                            max_value=121,
                            value=7,
                            step=1,
                            )


    def query_top_rows_per_year(data, n_top_rows):
        df_agr = pd.DataFrame(columns=data.columns)

        for i in data["Year"].unique():
            df_tmp = data[data.Year == i].sort_values(by=['TotAl_PerCapita'], ascending=False).head(n_top_rows)
            df_agr = df_agr.append(df_tmp, ignore_index=True)

        return df_agr


    sorted_data = query_top_rows_per_year(df_w, n_top)

    anim_pl = px.bar(sorted_data, x="TotAl_PerCapita", y="Entity",
                     animation_frame="Year",
                     animation_group="Entity",
                     range_x=[0, 20],
                     orientation="h",
                     labels={"TotAl_PerCapita": "Alcohol per capita",
                             "Entity": "Country"},
                     height=500,
                     title="Top-X coutries by alcohol consumption",
                     color_discrete_sequence=["teal"])
    anim_pl.update_layout(
        title_font=dict(size=20),
        font_size=15,
    )

    anim_pl.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    anim_pl.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 3500
    st.plotly_chart(anim_pl)

    st.markdown("""
    In this animated graph, we see that the world is not standing still, and many developed countries are leaving the top in alcohol consumption. Perhaps this is due to the fact that people have found a substitute for alcohol :)
    """)
