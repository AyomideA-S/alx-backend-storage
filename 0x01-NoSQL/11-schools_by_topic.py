#!/usr/bin/env python3
""" Where can I learn Python? """
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Find by documents specific value (topic) in a collection
    """
    return mongo_collection.find({"topics":  {"$in": [topic]}})
