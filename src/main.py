#This will be the SSMIF implementation of the Black-Litterman portfolio allcoation model for the purpose of 
#determining sector weightings in our portfolio

#We will need to calculate / define several vectors of values in order to use the black litterman equation

#Implied Equilibrium Returns (I) of our assets
#Coviariance matrix of the excess returns of the assets in question (E) 
#The relative market capitalizations of the assets in our model (w)
#The risk aversion coefficient (L)
#a constant (T)
#The variance of the error terms of our predictions (W) 
#A vector of views on stocks (Q)
#Lastly, a matrix relating our views to the assets we have chosen (P)

#So, lets start this off by trying to caluclate everything from the example we were given in the black litterman paper


#Views:
#International Developed Equity  will have an absolute excess return of 5.25% : confidence 25%
#International Bonds will outperform US Bonds by 25 basis points : Confidence 65%
#US Large Growth and US Small Growth will outperform US Large Value and US Small Value by 2% : Confidence 65%

#Note: the difference in return between inernational bonds and us bonds is supposed to be .59% so the view actually 
#represents International Bonds underperforming with respect to US Bonds - So we would expect the model to tilt away 
#from the international bonds and towards the US bonds

#By the same token, US large and small growth were supposed to outperform the US large and small value
#by 2.47% so we can say that US growth is underperforming 

#Now we define Q, our view vector, and the historical returns of all of our assets

Q = [5.25,
    .25,
    2]
e = [0,
    0,
    0]
Q = Q + e

#realistically, the views are added to some random error term set by the confidence of the view

#Now, the variance of the error terms e is what really is necesarry for the black litterman model
#remember, each e is a random distribution with mean 0 and variance sigma^2

#the omega matrix is a diagonal matrix of the variances of our error terms with all of the other locations being 0
#this is very pseudo codey
W = populateDiagonal(e.variance())




