from fraudTransaction.entity.config_entity import DataIngestionConfig
import os,sys
from fraudTransaction.exception import housingException
from fraudTransaction.logger import logging
from fraudTransaction.entity.artifact_entity import DataIngestionArtifact
import tarfile
import numpy as np
from six.moves import urllib
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit