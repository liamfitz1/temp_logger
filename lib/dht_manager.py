#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 09:46:25 2026

@author: Liam
"""
import time
import machine
import dht


class DHTManager:
    """DHT Module reads temperature and humidity."""
    def __init__(self, gpio_pin):
        self.sensor = dht.DHT11(machine.Pin(gpio_pin))
        self.__last_measure = time.ticks_ms()
        self.__temperature = None
        self.__humidity = None
        self._ensure_measure()

    def _ensure_measure(self, retries=5):
        """Function delays reading from the DHT Module to prevent errors."""
        for _ in range(retries):
            if time.ticks_diff(time.ticks_ms(), self.__last_measure) >= 2000:
                try:
                    self.sensor.measure()
                    self.__temperature = self.sensor.temperature()
                    self.__humidity = self.sensor.humidity()
                    self.__last_measure = time.ticks_ms()
                except OSError as e:
                    print(f"DHT read failed: {e}")
                else:
                    print("Measurement OK:", 
                          self.__temperature, self.__humidity)
                    break
            else:
                time.sleep(2)

    def get_temp_c(self):
        """Getter which returns temperature as C."""
        if time.ticks_diff(time.ticks_ms(), self.__last_measure) <= 2000:
            self._ensure_measure()
        return self.__temperature

    def get_temp_f(self):
        """Getter which returns temperature as C, to convert to F."""
        if time.ticks_diff(time.ticks_ms(), self.__last_measure) <= 2000:
            self._ensure_measure()
        return self.__temperature

    def get_humidity(self):
        """Getter returns humidity %."""
        if time.ticks_diff(time.ticks_ms(), self.__last_measure) <= 2000:
            self._ensure_measure()
        return self.__humidity
