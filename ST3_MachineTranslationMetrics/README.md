
# AmericasNLP 2025 Shared Task 3: Machine Translation Metrics for Indigenous Languages

The AmericasNLP 2025 Shared Task on machine translation metrics for Indigenous languages is a competition intended to motivate the advancement of automatic evaluation metrics for machine translation, with a focus on translation into Indigenous languages. Participants will build metrics to evaluate the quality of translations from Spanish into Guarani, Bribri, and Nahuatl. 

[Registration form](https://docs.google.com/forms/d/e/1FAIpQLSfmV9gyab03pGGzzDJ9DohOf9AkDaZf_94RvTroqrGwJqr0VQ/viewform?usp=sharing)

## Update:

3/5: Due to demand, we are extending the deadline of submission to 3/12/2015. The following deadlines/dates will be announced shortly.

3/1: Test data added.

2/4: 'Semantics' and 'Fluency' scores provided for the dev set in case the may be of use, note that 'Score' is their average and what we use to calculate correlations.

1/25: Development sets, baselines, and evaluation script added.



## Submission Guideline
Please send all your system outputs to americas.nlp.workshop@gmail.com. The subject of your email should be "AmericasNLP2025_SharedTask3; Shared Task Submission; ". The content of your submission email should be as follows:

Line 1: Team name 

Line 2: Names of all team members


Line 3: All languages you are sending submissions for in order of your choice (we will use that to double-check that we got all files you intended to send)

[optional] Line 4: A link to a GitHub repository with code that can be used to reproduce your results. This is not required in order to participate in the shared task, but it’s strongly encouraged. 


Please attach all output files to your email as a single zip file, named after your team, e.g., "TheGaugeCrew.zip". Within that zip file, the individual files should be named ".results.". The language code should be the same as used in the corresponding evaluation set names. The version number is in case you want to submit the outputs of multiple versions of your metric; it should be a single-digit (please don't submit more than 9 options per language!). The output file has all the scores of the test data in separate lines. 



## Baselines
The following are the Spearman's and Pearson's coefficients of the baseline metrics (BLEU and ChrF++) for the development sets, rounded to 4 decimal places.

<table>
  <tr>
    <th colspan="1"></th>
    <th colspan="3">Spearman</th>
    <th colspan="3">Pearson</th>
  </tr>
  <tr>
    <td></td>
    <td>Bribri</td>
    <td>Guarani</td>
    <td>Nahuatl</td>
    <td>Bribri</td>
    <td>Guarani</td>
    <td>Nahuatl</td>
  </tr>
  <tr>
    <td>BLEU</td>
    <td>0.3379</td>
    <td> 0.4694</td>
    <td>0.3813</td>
    <td>0.2890</td>
    <td>0.3797</td>
    <td>0.4430</td>
  </tr>
  <tr>
    <td>ChrF++</td>
    <td>0.4696</td>
    <td>0.6684</td>
    <td>0.6257</td>
    <td>0.3739</td>
    <td>0.6390</td>
    <td>0.5900</td>
  </tr>
</table>
