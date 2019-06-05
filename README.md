# Website for the Asian Pacific Mathematics Olympiad

![APMO LOGO](/static/apmologo.gif "Logo Title Text 1")

The Asian Pacific Mathematics Olympiad (APMO) is a mathematical competition for countries in the Pacific-Rim Region.
      
The APMO started in 1989. It has the following aims:
  
- Discovering, encouraging and challenging mathematically gifted high-school students.
- Fostering friendly international relations and cooperation between students and teachers throughout the region.
- Creating opportunities for the exchange of information on school syllabi and practice.
- Encouraging and supporting the mathematical involvement with Olympiad type activities in the participating countries and other countries of the region.

The website is hosted at http://www.apmo-official.org. This is the GitHub repository to manage and contribute to the website. 

## How the website works

The website is served with a combination of the following technologies:

- Flask for routing - http://flask.pocoo.org/
- Jinja2 for templating - http://jinja.pocoo.org/
- Booststrap for visual appearance  - https://getbootstrap.com/
- MathJax for beautiful mathematics - https://www.mathjax.org/
- Anaconda (pandas, seaborn) for data analysis and report creation - https://www.anaconda.com/

If you want to run a local version for development, my strong recommendation is that you get Anaconda and replace the Boostrap and MathJax CDNs with local intallations.

## How to contribute

You can contribute to the project in several ways. We need help with the following:

- Transform old result files (in PDF) to the more data-friendly .csv format
- Explore the data that we have and get new insights
- Help with the general maintenance of the website (typos, corrections, etc)

## The Web Development part

- The Flask 

## The Data part

For each year:

- Scores by person (best)
- Report of medals
- Report by countries
- Report of problems

For each country

- Number of medals per year
- Scores by person

Problems

- Problem statements
- Problem solutions

## Licencing

As of now, 