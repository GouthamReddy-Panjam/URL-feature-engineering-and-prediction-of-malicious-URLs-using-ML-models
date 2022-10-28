import pickle
loaded_model = pickle.load(open("XGBoostClassifier.pickle.dat", "rb"))

#importing required packages for this module
import pandas as pd
testurldata = pd.read_csv("testing.csv").sample(n=2).copy()
testurldata = testurldata.reset_index(drop=True)
testurldata.columns=["URLs"]

print(testurldata.head())

from urllib.parse import urlparse
import pandas as pd
import requests
from features import web_traffic
from features import domainAge, domainEnd, forwarding, getDepth, getDomain, getLength, haveAtSign, havingIP, httpDomain, iframe, mouseOver, prefixSuffix, redirection, rightClick, tinyURL
import whois

def featureExtraction(url):
    features = []
    # Address bar based features (8)
    features.append(havingIP(url))
    features.append(haveAtSign(url))
    features.append(getLength(url))
    features.append(getDepth(url))
    features.append(redirection(url))
    features.append(httpDomain(url))
    features.append(tinyURL(url))
    features.append(prefixSuffix(url))

    # Domain based features (4)
    dns = 0
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        dns = 1

    features.append(dns)
    features.append(web_traffic(url))
    features.append(1 if dns == 1 else domainAge(domain_name))
    features.append(1 if dns == 1 else domainEnd(domain_name))

    # HTML & Javascript based features (4)
    try:
        response = requests.get(url, timeout=3)
    except:
        response = ""
    features.append(iframe(response))
    features.append(mouseOver(response))
    features.append(rightClick(response))
    features.append(forwarding(response))
    return features


# Extracting the feautres & storing them in a list
features = []
for i in range(0, 2):
    url = testurldata['URLs'][i]
    print(f'{i+1} {url}')
    features.append(featureExtraction(url))
    

# converting the list to dataframe
feature_names = ['Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection',
                 'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic',
                 'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over', 'Right_Click', 'Web_Forwards']

test_urls_features = pd.DataFrame(features, columns=feature_names)
print(test_urls_features.head())


y_pred = loaded_model.predict(test_urls_features)
print("THe output is ",y_pred)