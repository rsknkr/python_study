# TV, halftime shows, and the Big Game
'''
Questions:
What are the most extreme game outcomes?
How does the game affect television viewership?
How have viewership, TV ratings, and ad cost evolved over time?
Who are the most prolific musicians in terms of halftime show performances?
'''

# The dataset we'll use was scraped and polished from Wikipedia.
# It is made up of three CSV files, one with game data, one with TV data, and one with halftime musician data
# for all 52 Super Bowls through 2018.

import pandas as pd
from IPython.display import display

# Load the CSV data into DataFrames
super_bowls = pd.read_csv('datasets/super_bowls.csv')
tv = pd.read_csv('datasets/tv.csv')
halftime_musicians = pd.read_csv('datasets/halftime_musicians.csv')

# Display the first five rows of each DataFrame
display(super_bowls.head())
display(tv.head())
display(halftime_musicians.head())

# For the Super Bowl game data, we can see the dataset appears whole except for missing values
# in the backup quarterback columns (qb_winner_2 and qb_loser_2), which make sense given most starting QBs
# in the Super Bowl (qb_winner_1 and qb_loser_1) play the entire game.

# From the visual inspection of TV and halftime musicians data, there is only one missing value displayed,
# but probably there are more. The Super Bowl goes all the way back to 1967, and the more granular columns
# (e.g. the number of songs for halftime musicians) probably weren't tracked reliably over time.

# An inspection of the .info() output for tv and halftime_musicians shows us that there are
# multiple columns with null values.

# Summary of the TV data to inspect
print(tv.info())

print('\n')

# Summary of the halftime musician data to inspect
print(halftime_musicians.info())

# Combined points distribution
# For the TV data, the following columns have a lot of missing values:
#   total_us_viewers (amount of U.S. viewers who watched at least some part of the broadcast);
#   rating_18_49 (average % of U.S. adults 18-49 who live in a household with a TV
#       that were watching for the entire broadcast);
#   share_18_49 (average % of U.S. adults 18-49 who live in a household with a TV in use
#       that were watching for the entire broadcast).

# For the halftime musician data, there are missing numbers of songs performed (num_songs) for about a third of the
# performances. There are a lot of potential reasons for these missing values. Was the data ever tracked? Was it lost
# in history? Is the research effort to make this data whole worth it? It's all possible. Let's take note of where
# the dataset isn't perfect and start uncovering some insights.

# We'll start by looking at combined points for each Super Bowl by visualizing the distribution.
# Let's also pinpoint the Super Bowls with the highest and lowest scores.

# Import matplotlib and set plotting style
from matplotlib import pyplot as plt

plt.style.use('seaborn')

# Plot a histogram of combined points
plt.hist(super_bowls["combined_pts"], bins=8)
plt.xlabel('Combined Points')
plt.ylabel('Number of Super Bowls')
plt.show()

# Display the Super Bowls with the highest and lowest combined scores
display(super_bowls[super_bowls['combined_pts'] > 70])
display(super_bowls[super_bowls["combined_pts"] < 25])

# Point difference distribution
# Most combined scores are around 40-50 points, with the extremes being roughly equal
# distance away in opposite directions. Going up to the highest combined scores at 74 and 75, we find two games
# featuring dominant quarterback performances. One even happened recently in 2018's Super Bowl LII where Tom Brady's
# Patriots lost to Nick Foles' underdog Eagles 41-33 for a combined score of 74.

# Going down to the lowest combined scores, we have Super Bowl III and VII, which featured tough defenses that
# dominated. We also have Super Bowl IX in New Orleans in 1975, whose 16-6 score can be attributed to inclement
# weather. The field was slick from overnight rain, and it was cold at 46 °F (8 °C), making it hard for the Steelers
# and Vikings to do much offensively. This was the second-coldest Super Bowl ever and the last to be played in
# inclement weather for over 30 years.

# Let's take a look at point difference now.
# Plot a histogram of point differences
plt.hist(super_bowls.difference_pts)
plt.xlabel('Point Difference')
plt.ylabel('Number of Super Bowls')
plt.show()

# Display the closest game(s) and biggest blowouts
display(super_bowls[super_bowls['difference_pts'] == 1])
display(super_bowls[super_bowls["difference_pts"] >= 35])

# Do blowouts translate to lost viewers?
# The vast majority of Super Bowls are close games. It makes makes sense since both teams are likely
# to be deserving if they've made it this far. The closest game ever was when the Buffalo Bills lost to
# the New York Giants by 1 point in 1991. The biggest point discrepancy ever was 45 points, where
# Joe Montana's led the San Francisco 49ers to victory in 1990, one year before the closest game ever.

# Do large point differences translate to lost viewers? We can plot household share (average percentage of U.S.
# households with a TV in use that were watching for the entire broadcast) vs. point difference to find out.

# Join game and TV data, filtering out SB I because it was split over two networks
games_tv = pd.merge(tv[tv['super_bowl'] > 1], super_bowls, on='super_bowl')

# Import seaborn
import seaborn as sns

# Create a scatter plot with a linear regression model fit
sns.regplot(x="difference_pts", y="share_household", data=games_tv)

# Viewership and the ad industry over time
# The downward sloping regression line and the 95% confidence interval for that regression suggest that
# bailing on the game if it is a blowout is common. Though it matches our intuition, we must take it
# with a grain of salt because the linear relationship in the data is weak due to our small sample size of 52 games.

# It's quite probable that many people are keen to see the halftime show, which is good news for the TV
# networks and advertisers. How have number of viewers and household ratings trended alongside halftime ad cost?
# We can find out using line plots that share a "Super Bowl" x-axis.
# Create a figure with 3x1 subplot and activate the top subplot
plt.subplot(3, 1, 1)
plt.plot(tv["super_bowl"], tv["avg_us_viewers"], color="#648FFF")
plt.title('Average Number of US Viewers')

# Activate the middle subplot
plt.subplot(3, 1, 2)
plt.plot(tv["super_bowl"], tv["rating_household"], color="#DC267F")
plt.title('Household Rating')

# Activate the bottom subplot
plt.subplot(3, 1, 3)
plt.plot(tv["super_bowl"], tv["ad_cost"], color="#FFB000")
plt.title('Ad Cost')
plt.xlabel('SUPER BOWL')

# Improve the spacing between subplots
plt.tight_layout()

# Halftime shows weren't always this great!
# We can see viewers increased before ad costs did.

# Maybe halftime shows weren't that good in the earlier years? The modern spectacle of the Super Bowl has
# a lot to do with the cultural prestige of big halftime acts.  It turns out Michael Jackson's Super Bowl XXVII
# performance, one of the most watched events in American TV history, was when the NFL realized the value of
# Super Bowl airtime and decided they needed to sign big name acts from then on out. The halftime shows before MJ
# indeed weren't that impressive, which we can see by filtering our halftime_musician data.

# Display all halftime musicians for Super Bowls up to and including Super Bowl XXVII
display(halftime_musicians[halftime_musicians['super_bowl'] <= 27])

# Who has the most halftime show appearances?
# Lots of marching bands. American jazz clarinetist Pete Fountain. Miss Texas 1973 playing a violin.
# Let's see all of the musicians that have done more than one halftime show, including their performance counts.
# Count halftime show appearances for each musician and sort them from most to least
halftime_appearances = halftime_musicians.groupby('musician').count()['super_bowl'].reset_index()
halftime_appearances = halftime_appearances.sort_values('super_bowl', ascending=False)

# Display musicians with more than one halftime show appearance
display(halftime_appearances[halftime_appearances['super_bowl'] > 1])

# Who performed the most songs in a halftime show?
# The world famous Grambling State University Tiger Marching Band takes the crown with six appearances.
# Beyoncé, Justin Timberlake, Nelly, and Bruno Mars are the only 2000s musicians with multiple appearances (two each).
# From our previous inspections, the num_songs column has lots of missing values:
#   A lot of the marching bands don't have num_songs entries.
#   For non-marching bands, missing data starts occurring at Super Bowl XX.

# Let's filter out marching bands by filtering out musicians with the word "Marching" in them
# and the word "Spirit" (a common naming convention for marching bands is "Spirit of [something]").
# Then we'll filter for Super Bowls after Super Bowl XX to address the missing data issue, then
# let's see who has the most number of songs.
# Filter out most marching bands
no_bands = halftime_musicians[~halftime_musicians.musician.str.contains('Marching')]
no_bands = no_bands[~no_bands.musician.str.contains('Spirit')]

# Plot a histogram of number of songs per performance
most_songs = int(max(no_bands['num_songs'].values))
plt.hist(no_bands.num_songs.dropna(), bins=most_songs)
plt.xlabel("Number of Songs Per Halftime Show Performance")
plt.ylabel('Number of Musicians')
plt.show()

# Sort the non-band musicians by number of songs per appearance...
no_bands = no_bands.sort_values('num_songs', ascending=False)
# ...and display the top 15
display(no_bands.head(15))

# Conclusion
# So most non-band musicians do 1-3 songs per halftime show. It's important to note that the duration of
# the halftime show is fixed (roughly 12 minutes) so songs per performance is more a measure of how many hit songs
# you have. JT went off in 2018, wow. 11 songs! Diana Ross comes in second with 10 in her medley in 1996.

# In this notebook, we loaded, cleaned, then explored Super Bowl game, television, and halftime show data. We
# visualized the distributions of combined points, point differences, and halftime show performances using
# histograms. We used line plots to see how ad cost increases lagged behind viewership increases. And we discovered
# that blowouts do appear to lead to a drop in viewers.

# This year's Big Game will be here before you know it. Who do you think will win Super Bowl LIII?
# 2018-2019 conference champions
patriots = 'New England Patriots'
rams = 'Los Angeles Rams'

# Who will win Super Bowl LIII?
super_bowl_LIII_winner = patriots
print('The winner of Super Bowl LIII will be the', super_bowl_LIII_winner)