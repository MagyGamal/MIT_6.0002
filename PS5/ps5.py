# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Magy Gamal Matta
# Collaborators (discussion):
# Time:
import math
import pylab
import re
import numpy

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models=[]
    for degree in degs:
        models.append(pylab.polyfit(x,y,degree))
    return models

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    var=0
    error=0
    mean=sum(y)/len(y)
    for i in range(len(y)):
        error+=(y[i]-estimated[i])**2
        var+=(y[i]-mean)**2
    Rsqr=1-(error/var)
    return Rsqr
    
def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        estYVals = pylab.polyval(model,x)
        Rsqr=r_squared(y,estYVals)
        pylab.figure()
        pylab.plot(x, y, 'bo',label = 'Measured points',scalex=False)
        pylab.plot(x, estYVals, 'r',label = "model")
        pylab.legend(loc="best")
        pylab.xlabel('Year')
        pylab.ylabel('Temperature in degree celsius')
        if len(model)-1>1:
            pylab.title("R2:"+str(Rsqr)+"Degree"+str(len(model)-1))
        else:
            seos=se_over_slope(x,y,estYVals,model)
            pylab.title("R2:"+str(Rsqr)+"Degree"+str(len(model)-1)+"\n Standard error over slope"+str(round(seos,2)))
            
def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    cities_avg=[]
    for year in years:
        cities_tmp=[]
        for city in multi_cities:
            cities_tmp.append(climate.get_yearly_temp(city, year).mean())
        cities_tmp=pylab.array(cities_tmp)
        cities_avg.append(sum(cities_tmp)/len(cities_tmp))
    return pylab.array(cities_avg)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_avg=[]
    avg=0
    for sample in range(len(y)):
        items=[]
        if sample < window_length-1:
            for i in y[0:sample+1]:
                items.append(i)
        else:
            for j in y[sample-window_length+1:sample+1]:
                items.append(j)
        avg=sum(items)/len(items)
        moving_avg.append(avg)
    return pylab.array(moving_avg)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    error=[]
    for i in range (len(y)):
        error.append((y[i]-estimated[i])**2)
    return math.sqrt(sum(error)/len(error))
    
def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """

    std_dev=[]
    for year in years:
        cities_yearly_tmp=[]
        for city in multi_cities:
            city_tmp=climate.get_yearly_temp(city, year)
            cities_yearly_tmp.append(city_tmp)
            days=len(city_tmp)
        national_tmp=[]
        for day in range(days):
            daily_tmp=0
            for City in range(len(multi_cities)):
                daily_tmp+=cities_yearly_tmp[City][day]
            daily_tmp=daily_tmp/len(multi_cities)
            national_tmp.append(daily_tmp)
        std_dev.append(numpy.std(national_tmp))
    return pylab.array(std_dev)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        estYVals = pylab.polyval(model,x)
        Rmse=rmse(y,estYVals)
        pylab.figure()
        pylab.plot(x, y, 'bo',label = 'Measured points')
        pylab.plot(x, estYVals, 'r',label ="Model")
        pylab.xlabel('Year')
        pylab.ylabel('degree celsius')
        pylab.legend(loc = 'best')
        pylab.title("Rmse:"+str(Rmse)+"Degree"+str(len(model)-1))
    
if __name__ == '__main__':

    # Part A.4
    
    climate=Climate("data.csv")
    x_train=pylab.array(TRAINING_INTERVAL)
    ydaily=[]
    yyearly=[]
    for year in x_train :
        ydaily.append(climate.get_daily_temp("NEW YORK", 1, 10, year))
        yyearly.append(climate.get_yearly_temp("NEW YORK",year).mean())
    ydaily=pylab.array(ydaily)
    yyearly=pylab.array(yyearly)
    model_1=generate_models(x_train, ydaily, [1])
    evaluate_models_on_training(x_train, ydaily, model_1)
    model_2=generate_models(x_train, yyearly, [1])
    evaluate_models_on_training(x_train, yyearly, model_2)
    
#    # Part B
    
    generaly=gen_cities_avg(climate,CITIES,TRAINING_INTERVAL)
    model_3=generate_models(x_train, generaly, [1])
    evaluate_models_on_training(x_train, generaly, model_3)
#            
#    # Part C
    
    y_avg=moving_average(generaly, 5)
    model_4=generate_models(x_train, y_avg, [1,2,20])
    evaluate_models_on_training(x_train, y_avg, model_4)
#
#    # Part D.2
    
    x_test=TESTING_INTERVAL
    y_2=gen_cities_avg(climate,CITIES,TESTING_INTERVAL)
    y_test=moving_average(y_2, 5)
    models_5=generate_models(x_train, y_avg, [1,2,20])
    evaluate_models_on_training(x_train, y_avg, models_5)
    evaluate_models_on_testing(x_test, y_test, models_5)

#    # Part E
    
    standard_dev=gen_std_devs(climate, CITIES, TRAINING_INTERVAL)
    y_3=moving_average(standard_dev, 5)
    model_6=generate_models(x_train, y_3, [1])
    evaluate_models_on_training(x_train, y_3, model_6)
