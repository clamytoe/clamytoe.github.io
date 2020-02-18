title: Rescaling Values
date: 2020-02-12 12:00
category: DataScience
slug: rescaling-values
author: Martin Uribe
summary: Quick discussion about rescaling values for data science

# Scaling Values

Today while reading Data Science Algorithms in a Week, from packt, I came across the concept of rescaling values so that when measuring their distances they would be more relavant. The dataset consisted of "House Ownership":

|Age|Annual income in USD|House ownership status|
|:--|:-------------------|:---------------------|
|23|50,000|Non-owner|
|37|34,000|Non-owner|
|20|100,000|Owner|
|35|130,000|Owner|
etc

The aim being to predict whether a person that is 50 years old with an income of $80,000, would own a home so that he could be targeted for home insurance.

kNN's are currently being covered and for this exercise a `k = 1` is to be used. Using either a Euclidean or Manhattan distance wouldn't matter because the distances between these values are too great. In comes rescalling!

The formula use is:

> **ScaledQuantity = (ActualQnatity-MinQuantity)/(MaxQuantity-MinQuantity)**

So for this dataset, both the **Age** and the **Annual income** wound have to be adjusted.

> **ScaledAge = (ActualAge-MinAge)/(MaxAge-MinAge)**

> **ScaledIncome = (ActualIncome-MinIncome)/(MaxIncome-MinIncome)**

After scaling, the adjusted dataset would look something like this:

|Age|Scaled age|Annual income in USD|Scaled annual income|House ownership status|
|:--|:---------|:-------------------|:------------|:---------------------|
|23|09375|50,000|2|Non-owner|
|37|53125|34,000|04|Non-owner|
|20|0|100,000|7|Owner|
|35|46875|130,000|1|Owner|
|50|9375|80,000|5|?|

Now an 1-NN algorithm with a Euclidean metric could easily be used to find out if the last person is more than likely to own a home. Without the rescaling, the algorithm would have yielded different results.

Keeping it short today, but hopefully it was a helpful tip!