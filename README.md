# Website for the Asian Pacific Mathematics Olympiad

![APMO logo](/static/apmologo.gif "Logo Title Text 1")

The Asian Pacific Mathematics Olympiad (APMO) is a mathematical competition for countries in the Pacific-Rim Region.
      
The APMO started in 1989. It has the following aims:
  
- Discovering, encouraging and challenging mathematically gifted high-school students
- Fostering friendly international relations and cooperation between students and teachers throughout the region
- Creating opportunities for the exchange of information on school syllabi and practice
- Encouraging and supporting the mathematical involvement with Olympiad type activities in the participating countries and other countries of the region

The website is hosted at http://www.apmo-official.org. This is the GitHub repository to manage and contribute to the website.

## How the website works

The website is served with a combination of the following technologies:

- Flask for routing - http://flask.pocoo.org/
- Jinja2 for templating - http://jinja.pocoo.org/
- Booststrap for visual appearance  - https://getbootstrap.com/
- MathJax for beautiful mathematics - https://www.mathjax.org/
- Anaconda (pandas, seaborn) for data analysis and report creation - https://www.anaconda.com/

If you want to run a local version for development, my strong recommendation is that you get Anaconda and replace the Boostrap and MathJax CDNs with local intallations.

## The Web Development part

The relevant files in the repository are:

- `webpage.py` is the Flask app that routes everything
- `templates/` is th directory with the Jinja2 templates

## The Data part

Since 2016, we have complete score tables that include countries, contestant names, detailed problem scores and gender. This is what we call a <i> full score table </i>. The ideal situation for a year is to have its full score table in a standard data format (`.csv` or `.xlsx`).

With a full score table we can generate many useful reports to be displayed on the website:

- Overview of APMO results over the years
- Detailed yearly report
    - General information of edition
    - Country rankings per year
    - Awards per year
    - Problem statistics
    - Detailed results by country
- Overview of results by country over the years
- Detailed results by country over the years

Unfortunately, for the pre-2016 period we only have partial information:

- There is very scarce information on the pre-2005 period. Most of it was obtained from old versions of the Australian Mathematics Trust Website.
- In the period 2005-2009 we only have information on the awards. We have full names and countries. TThe awards are in CSV form but the name of the contestants are in PDF form.
- In the period 2010-2015 we have information on awards (as above), country rankings per year and general information on the edition. This is currently in PDF form.

The relevant files in the repository are:

- `data/` has Jupyter notebooks for processing data and folders with data
- `data/results_pre2016` has the PDFs with results from the period before 2016
- `data/data_clean` contains the clean score tables from 2016 onwards
- `data/reports` is the directory where the yearly reports are created

## How to contribute

You can contribute to the project in several ways. We need help with the following:

- Provide any kind of APMO results for the pre-2005 era
- Provide your country individual scores for the 2010-2015 era
- Provide scores or country rankings for the 2005-2016 era
- Provide full texts of the regulations for the pre-2015 era 
- Transform files from the 2005-2015 era from PDF to a data-friendly .csv format
- Explore the data that we have and get new insights
- Help with the general maintenance of the website (typos, corrections, etc)

## Contributors

- Carlos Yuzo Shine - Information Brazil 2012-2015
- Richard Bollard - Information Australia 1989-2009
- OBM Webpage - Names Brazil contestants 2010-2011
- Richard Eden - Solutions APMO 1990 and 1995-2003
- Daniel Redd - Solutions 2004
- Carlos Yuzo Shine and Brazil team - Solutions APMO 1989, 1991-1994, 2000, 2004
- Richard Eden - Detailed information Philippines 2008-2015
- Angelo Di Pasquale - More details on Australia participations 1989-2007

## Licencing

As of now, please send any requests to use part of this data or code to Leonardo Martínez (`leomtz@ciencias.unam.mx`).