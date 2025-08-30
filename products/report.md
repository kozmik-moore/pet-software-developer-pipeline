# Summary analysis

*This report can also be found at the end of the [Jupyter notebook](../code/notebook.ipynb).*

*The Data*

This analysis was conducted on data supplied by HappyPaws from their app between April 1, 2022 and December 30, 2023, a period of 21 months. This dataset contains records for 1878 pet owners, each recording for a single pet. Pet type, pet activities of health and non-health oriented varieties were recorded, as were owner ages, activity durations, and resolutions for health issues.

*Observations*

Pet ownership among users of this app is dominated by those who own fish, hamsters, and rabbits. This contrasts with the statistics of the American Veterinary Medical Association, which has dog and cat proportions at 46% and 32%, respectively; meanwhile, fish (2.9%), hamsters (1%) and rabbits (0.7%) rank fairly low in terms of ownership shares.

By age group, pet ownership is fairly consistent, proportionally. The only interesting groups are:
- rabbits, which are popular among owner age groups 26-35 and 66 and older
- cats, which enjoy less popularity in the 66 and older crowd
- and the 56-65 age group who favor dogs at higher rates and fish at lower rates than the rest of the owner ages groups or pet types

For planned health activities, annual checkups make roughly half of medical records in the app, on average. This holds by pet type, mostly.
Zooming in on annual checkups, I found that records for dogs were submitted more often than other pet types while cats and fish saw the longest lull between records. Duration between records was fairly consistent among different age groups.
Additionally health activities were recorded fairly consistently per month over the period examined.


When looking at non-health activities ("playing", "walking", "resting"), playing was the most common activity recorded but not by much over the other activities. This held true by pet type.

Analyzing activity durations yielded very little interesting information that was not already obvious from other visualizations (e.g. fish get quite a bit of "walking" and "playing" time).

Looking at these activities by owner age group and pet type, I found that dogs and cats were pet types that saw average activity counts per month that were more consistently lower while fish, hamsters, and rabbits were more consistent across the age groups. It is worth noting that, for playing and walking, the (dogs, 56-65) age group shines in record counts, though that may be due to sheer volume.

Distribution of durations between records for these activities clustered around two values for different groups. For pet types, cats, rabbits, and hamsters saw records around every 130-150 days, on average, while dogs and fish saw closer to every 275 days, on average. For owner age groups, groups between 26 and 55 clustered around 130 days, while the other age groups clustered around 220 days.

When focusing on duration between playtime records, there were no striking trends other than that there are many lulls and peaks for all pairings of pet type and owner age group across the time period examined. And, sometimes, these lulls lasted for consecutive months.

## Recommendations

To increase app use and consistency of app use, a few things should be done.

Engagement with cat and dog owners is very low, relative to the American population. Campaigns to engage with these groups need to be mounted, which would increase overall user volume.

Efforts to encourage owners to record activities more often should be undertaken. It is hard to imagine that owners do not interact with pets for months at a time, so it must be that they are not using the app very often. Creating incentives to record more often should be considered, as well as instituting reminders or alarms in the app.

Walking and playing saw high counts among animals that were not dogs or cats, which is interesting (especially as regards fish!). An effort should be made to see what owners are experiencing or doing when they make these records, to understand how owners are interacting with the app. Furthermore, it would be useful to find out what specific kinds of activities owners are classing into "playing", "resting", and "walking" and what criteria they use to make that determination. Offering sub-activities to choose from would improve data quality and might yield more interesting data about activity durations.

Other things that could improve data quality include:
- composition of owner households: are these single people, families, childless couples?
- whether these app users are single-pet households
- pet ages