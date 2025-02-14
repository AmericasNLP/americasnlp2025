# AmericasNLP 2025 Shared Task on Machine Translation into Indigenous Languages

Welcome to the Machine Translation Shared Task into Indigenous Languages! We are excited to host the **4th iteration** of the Shared Task. 


# Table of Contents
1. [Registration](#registration)
2. [Important Dates](#important_dates)
3. [Shared Task Description: Tasks and Rules](#shared-task-description-tasks-and-rules)
4. [Languages](#languages)
5. [Links to Prior Iterations](#links-to-prior-iterations)
6. [Contact](#contact)
7. [Baseline System](#baselines)

## Registration

Please use the following link to indicate your interest in participating: https://forms.gle/gXRoa9pr6K75Tgce7

## Important Dates
- Release of training and development sets: January 30th, 2025
- Release of baseline systems and baseline results: February 15th, 2025
- Release of test inputs: March 1st 2025
- Submission of results (shared task deadline): March 25th, 2025
- Announcement of winners: April 4th, 2025
- Submission of system descriptions papers: April 8th, 2025
- Notification of acceptance: April 11th, 2025
- Camera-ready papers due: April 14th, 2025
- Workshop: May 4th, 2025



## Shared Task Description: Tasks and Rules:

We are making some exciting changes and additions to the Shared Task for 2025!

**New for 2025**:

- [New languages!](#languages)
- [New translation direction: translation into Spanish](#new-translation-directions)


### New Translation Directions

For 2025, we are expanding the shared task to include both translation into an Indigenous language (from Spanish) **as well as** translation from an Indigenous language into Spanish. These different directions will be represented as two tracks within the shared task:

- **Track 1**: Systems which translate from Spanish into an Indigenous language (Es-XX)
- **Track 2**: Systems which translate from an Indigeous language into Spanish (XX-Es)


### Rules

The Machine Translation Shared Task will be broken down into 2 separate competitions:

- **Track 1** : Machine translation from Spanish into an Indigenous language (*similar to prior ST iterations*)
- **Track 2** : Machine translation from an Indigenous language into Spanish

Participants can submit to as many tracks as they wish. The same system can be submitted to multiple tracks if desired.

The following rules apply to all tracks:

1. Training on the development set is **not** allowed. Specifically, the dev set should only be used to evaluate a current model; as a rule of thumb, the model outputs at inference time should be consistent with or without access to the development set. If you have any questions or would like to clarify a specific approach, please contact the organizers!   
2. Using the [AmericasNLI](https://aclanthology.org/2022.acl-long.435.pdf) test set for hyperparameter tuning or any form of decision making is not allowed. 
3. Evaluation will be done using the `evaluate.py` script. The final order of teams will be selected using average **ChrF++** across all languages. Note that prior years have used *ChrF*. We accept submissions that do not cover all languages -- in these cases, the average ranking for these systems will be calculated using a *ChrF++* of `0.0` for each unsupported language. In this case, please reach out if you would like your system omitted from the overall rankings -- we still encourage you to submit a system description paper in this case!
4. We will **not** allow multiple submissions which rely on the same model (by same, we mean the same exact weights and architecture). As an example, if a submitted system relies on a specific model (say Model A), a second submission which relies on a new model (Model B) for some languages, but falls back to Model A given dev set performance, is not allowed. In this case, there are two allowed possibilites: (1) submit Model B as an independent submission with no fallback to Model A or (2) withdraw the original submission of Model A, and submit the system which relies on both Model A and Model B as a single submission. As a rule of thumb, two submissions from the same team should not have the same exact performance for a given language unless by chance.
5. **(New for 2025)**: While we will accept and present results from all submissions, only submissions which rely solely on models with **open-source weights** will be considered in the final shared task ranking.



## Languages

We are excited to add two new languages for the 2025 Shared Task: `Wayuunaiki (guc)` and `Awajun (agr)`, 

The complete list of languages is below:

| ISO| Language |
---|---|
agr | **Awajun**
aym | Aymara 
bzd |Bribri
cni | Asháninka 
ctp | Chatino 
grn | Guarani 
guc | **Wayuunaiki**
hch | Wixarika 
nah | Nahuatl 
oto | Otomí 
quy | Quechua 
shp | Shipibo-Konibo 
tar | Rarámuri 

## Links to Prior Iterations

For reference to the prior shared tasks, winning submissions, and further analysis on the data and results, please see the prior Findings and system description papers, linked below:

| Year | Findings | System Description Papers |
|--|--|--|
| 2021| [Findings](https://aclanthology.org/2021.americasnlp-1.23/) | [Submitted Systems](https://aclanthology.org/volumes/2021.americasnlp-1/) |
| 2023| [Findings](https://aclanthology.org/2023.americasnlp-1.23/) | [Submitted Systems](https://aclanthology.org/volumes/2023.americasnlp-1/) |
| 2024| [Findings](https://aclanthology.org/2024.americasnlp-1.28/) | [Submitted Systems](https://aclanthology.org/volumes/2024.americasnlp-1/) |


## Contact

We are more than happy to answer any questions regarding the workshop or shared task, please email us at [americas.nlp.workshop@gmail.com](malito:americas.nlp.workshop@gmail.com). Alternatively, [join our Slack channel](https://join.slack.com/t/americasnlp/shared_invite/zt-2c3lstrpe-n6DXqZyGVXVqDaGiM7mbHA).



## Baselines

## Baseline Systems 

### From Spanish

This year we provide the same two baseline systems, based on the best contenders of the 2023's results. In last year's edition, no overall system outperformed the current baselines.

- [Sheffield](https://aclanthology.org/2023.americasnlp-1.21/): you can find more information [here](baselines/sheffield)
- [Helsinki](https://aclanthology.org/2023.americasnlp-1.20/): you can find more information [here](baselines/helsinki)

We provide ChrF++ results computed with the [evaluate.py](evaluate.py) script.

## Results

### Development set

Results for development sets in **ChrF++**: 

| ISO| Language | Helsinki | Sheffield
---|---|----|----
agr | **Awajun** | -- | --
aym | Aymara | 32.63 | 34.28
bzd |Bribri | 22.65 | 25.03
cni | Asháninka | 25.68 | 26.34
ctp | Chatino |  30.06 | 37.33
gn | Guarani | 34.74 | 32.17
guc | **Wayuunaiki** | -- | --
hch | Wixarika | 27.98 | 27.98
nah | Nahuatl | 26.45 | 25.58
oto | Otomí |  13.10 | 12.69
quy | Quechua | 28.78 | 30.22
shp | Shipibo-Konibo | 30.59 | 28.39
tar | Rarámuri | 17.58 | 16.91

### Test set

Results for test sets in **Chrf++**:

| ISO| Language | Helsinki | Sheffield
---|---|----|----
agr | **Awajun** | -- | --
aym | Aymara | 29.36 | **31.84**
bzd |Bribri | 23.47 | **25.58**
cni | Asháninka | **24.92** | 24.76
ctp | Chatino |  29.84 | **37.05**
gn | Guarani | **37.02** | 35.76
guc | **Wayuunaiki** | -- | --
hch | Wixarika | **28.67** | 28.28
nah | Nahuatl | 22.78 | **23.28**
oto | Otomí |  **13.32** | 12.87
quy | Quechua | 28.81 | **34.01**
shp | Shipibo-Konibo | **30.21** | 30.06
tar | Rarámuri | **16.98** | 16.25

### Into Spanish

Coming soon!