import os, sys
from sensor.utils import get_collection_as_dataframe


if __name__ == "__main__":
     try:
          get_collection_as_dataframe(db_name="aps", collection_name="sensor")
     except Exception as e:
          print(e)
