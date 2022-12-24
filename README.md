# Pokemon Statistical Analysis

![logo](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/pokemon_logo.png)



## Project Description
In this mini analysis, I wanted compare the power statistics of different pokemon types and see if there is a significant difference between them.
Check out ``script/analysis.ipynb`` to view the full analysis on jupyter notebook

Power statistics here refer to:
- Hit points
- Attack
- Defense
- Special Defense
- Special Attack
- Speed

There are 18 different pokemon types.

![types](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/pokemon_type.png)

## Getting the data
According to [PokeAPI](https://pokeapi.co/), the data for sword and shield (generation 6) might be inaccurate. As such, we will just use the data from generation 1 to 5 for this analysis. Check out ``script/pokemon_scraper.py`` to find out how the data was obtained   

## Preprocessing
Some pokemons belong to two different types.

For example: Bulbasaur is both grass and poison type.

| name  | hp | attack | defense | special_attack | special_defense | speed | types | 
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| bulbasaur  | 45  | 49  | 49  | 65  | 65  | 45  | grass, poison |

I duplicated the information so that each type is being represented

| name  | hp | attack | defense | special_attack | special_defense | speed | types | 
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| bulbasaur  | 45  | 49  | 49  | 65  | 65  | 45  | grass |
| bulbasaur  | 45  | 49  | 49  | 65  | 65  | 45  | poison |

For a more accurate representation of the types, I also excluded legendary pokemons, as they are much more powerful.

![legendary](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/legendary.png)

## Distribution
Normality is an important assumption for many statistical tests. Let's first examine their distribution.

Overall, the distribution for attack and special attack are quite normally distributed. On the other hand, the distribution of hit points, defense, special defense and speed are right skewed. 

![overall_dist](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/overall_distribution.png)

Breaking the distribution down to individual types, we see that the distribution are quite similar. It will be quite difficult to tell them apart given just these six features.

![type_dist](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/types_distribution.png)

## Kurtosis
To find our more about the tail distribution, we can use kurtosis measure. Kurtosis is a measure that describes the shape of the distribution's tails in relation to its overall shape. Here, I used the scripy.stats package to calculate the kurtosis value. I set ``fisher=True`` to normalise the value so that a distribution similar to a normal distribution would have kurtosis = 0.0 (Mesokurtic). Anything > 0 would indicate that the distribution has long tails.

![kurtosis](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/kurtosis.png)

## Radar Plot

Another way of gaining an intuition of the statistics for each type is through the radar plot. Using the average value for each type, we can obtain a radar plot.

![radar](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/radar_plot.png)

## Are the differences significant?
There are some assumptions that we have to satisfy in order to use parametric tests
- Observations in each group are independent and identically distributed
- Observations in each group are normally distributed
- Observations in each sample have same variance

### Indepedent and identically distributed
Since there is no connection between the observations, the samples are independent. Identically distributed relates to the probability distribution that describes the characteristic you are measuring. One probability distribution should adequately model all values you observe in sample. Since there doesn't seem to be any trends in the data, we assume that the observations are identically distributed.

### Normally distributed
Earlier, we have seen that some distributions are skewed. We could try various transformations to obtain a normal distribution

![transform_hp](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/transform_hp.png)

![transform_attack](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/transform_attack.png)

![transform_defense](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/transform_defense.png)

![transform_special_attack](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/transform_special_att.png)

![transform_special_defense](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/transform_special_def.png)

![transform_speed](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/transform_speed.png)

We can use Shapiro-Wilk test to test for normality. Since the number of samples for each type is small (<50), I decided to use Shapiro-Wilk instead of Kolmogorov Smirnov. Unfortunately, the normality test fails for some types.

### Equal Variance
We can use the Levene's/Bartlett's test to test for equality of variance between groups. The results show that the groups are of unequal variance. 

## Kruskal Wallis Test
We have to use non-parametric test since the assumptions are not met. Here, we can use Kruskal Wallis Test. It is a non-parametric version of ANOVA and it tests whether the distributions of two or more indepndent samples are equal.  

The hypotheses are:   
- $H_{0}$: Distributions of all groups are equal 
- $H_{1}$: Distributions of all groups are unequal  

We obtain a result of pvalue <0.05 for all six factors. To determine which groups are different, we can conduct a post-hoc test.

## Dunn's Test
To use the Dunn's Test to run a posterior analysis test and compare pairwise group differences to determine which groups are different.  

The hypotheses are:  

- $H_{0}$: All means are the same $(\mu_{i} = \mu_{j})$     
- $H_{1}$: All means are not the same $(\mu_{i} \neq \mu_{j})$

To compare the results, I plotted a heatmap.

- For hp
![hp_dunn](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/hp_dunn_test.png)

- For attack
![attack_dunn](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/attack_dunn_test.png)

- For defense
![def_dunn](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/defense_dunn_test.png)

- For special attack
![special_att_dunn](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/special_attack_dunn_test.png)

- For special defense
![special_def_dunn](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/special_defense_dunn_test.png)

- For speed
![speed_dunn](https://github.com/Joanna-Khek/pokemon-statistical-analysis/blob/main/images/speed_dunn_test.png)

# Conclusion
- **HP**: The differences between types are not too different with the exception of bug vs ground and bug vs normal.
- **Attack**: Overall, the attack power of fighting type is very different from bug, electric, fairy, grass psychic and water. The attack power of fairy and psychic pokemons are also very different from many dark, dragon, ground, rock and steel type.
- **Defense**: The defense power of rock and steel type is very different from all other types except dragon and ground.
- **Special Defense**: Overall, the special defense power of all types are not too different with the exception of psychic.
- **Special Attack**: With the exception of dark, dragon, fairy, flying, poison and steel, the special attack of all other types are significantly different from some other types.
