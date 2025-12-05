#!/usr/bin/env python3
"""
Master Script: Generate All Amsterdam Datasets

Generates all datasets in the correct order:
1. Weather (foundation)
2. Events (can reference weather)
3. Bus Schedules (independent)
4. Bookings (correlates with events and weather)

All datasets span: November 2023 - November 2025
All datasets focus on: Amsterdam only
"""

import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from generate_weather import generate_weather
from generate_events import generate_events
from generate_bus_schedules import generate_bus_schedules
from generate_bookings import generate_bookings, generate_accommodations
from generate_web_analytics import generate_web_analytics

def main():
    """Main function to generate all datasets."""
    generate_weather()
    generate_events()
    generate_bus_schedules()
    
    accommodations_df = generate_accommodations()
    generate_bookings(accommodations_df)
    generate_web_analytics()


if __name__ == '__main__':
    main()

