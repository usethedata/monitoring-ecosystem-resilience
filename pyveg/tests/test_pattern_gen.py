"""
Tests for the functions and methods in pattern_generation.py
"""

import pytest

from pyveg.src.pattern_generation import (
    calc_plant_change,
    calc_surface_water_change,
    calc_soil_water_change
)


def test_plant_change_zero():
    plant_biomass = 0.
    soil_water = 0
    grazing_loss = 0.3
    senescence = 0.1
    growth_constant = 0.05
    uptake = 10.
    uptake_saturation = 3.
    assert(calc_plant_change(plant_biomass,
                             soil_water,
                             uptake,
                             uptake_saturation,
                             growth_constant,
                             senescence,
                             grazing_loss)==0)



def test_plant_decreases():
    # first get a benchmark
    plant_biomass = 90.
    soil_water = 0
    grazing_loss = 0.3
    senescence = 0.1
    growth_constant = 0.05
    uptake = 10.
    uptake_saturation = 3.
    change_1 = calc_plant_change(plant_biomass,
                             soil_water,
                             uptake,
                             uptake_saturation,
                             growth_constant,
                             senescence,
                             grazing_loss)
    # now increase grazing_loss
    grazing_loss = 0.5
    change_2 = calc_plant_change(plant_biomass,
                             soil_water,
                             uptake,
                             uptake_saturation,
                             growth_constant,
                             senescence,
                             grazing_loss)
    assert(change_1 > change_2)
    # now increase senescence
    senescence = 0.2
    change_3 = calc_plant_change(plant_biomass,
                             soil_water,
                             uptake,
                             uptake_saturation,
                             growth_constant,
                             senescence,
                             grazing_loss)
    assert(change_2 > change_3)


def test_plant_increases():
    # first get a benchmark
    plant_biomass = 90.
    soil_water = 0
    grazing_loss = 0.3
    senescence = 0.1
    growth_constant = 0.05
    uptake = 10.
    uptake_saturation = 3.
    change_1 = calc_plant_change(plant_biomass,
                                 soil_water,
                                 uptake,
                                 uptake_saturation,
                                 growth_constant,
                                 senescence,
                                 grazing_loss)
    # now increase the soil water
    soil_water = 3.0
    change_2 = calc_plant_change(plant_biomass,
                                 soil_water,
                                 uptake,
                                 uptake_saturation,
                                 growth_constant,
                                 senescence,
                                 grazing_loss)
    assert(change_2 > change_1)


def test_surface_water_zero():
    # zero rainfall, zero starting water
    rainfall = 0.
    plant_biomass = 90.
    surface_water = 0.
    frac_available = 0.1
    bare_soil_infilt = 0.15
    infilt_saturation = 5
    change = calc_surface_water_change(surface_water,
                                       plant_biomass,
                                       rainfall,
                                       frac_available,
                                       bare_soil_infilt,
                                       infilt_saturation)
    assert(change==0)


def test_surface_water_more_rain():
    # First get a benchmark
    rainfall = 0.
    plant_biomass = 90.
    surface_water = 0.
    frac_available = 0.1
    bare_soil_infilt = 0.15
    infilt_saturation = 5
    change_1 = calc_surface_water_change(surface_water,
                                         plant_biomass,
                                         rainfall,
                                         frac_available,
                                         bare_soil_infilt,
                                         infilt_saturation)
    # now increase rainfall
    rainfall = 1.4
    change_2 = calc_surface_water_change(surface_water,
                                         plant_biomass,
                                         rainfall,
                                         frac_available,
                                         bare_soil_infilt,
                                         infilt_saturation)
    assert(change_2 > change_1)


def test_surface_water_more_absorption():
    # First get a benchmark
    rainfall = 1.4
    plant_biomass = 90.
    surface_water = 3.
    frac_available = 0.1
    bare_soil_infilt = 0.15
    infilt_saturation = 5
    change_1 = calc_surface_water_change(surface_water,
                                         plant_biomass,
                                         rainfall,
                                         frac_available,
                                         bare_soil_infilt,
                                         infilt_saturation)
    # now increase soil absorption
    bare_soil_infilt = 0.2
    change_2 = calc_surface_water_change(surface_water,
                                         plant_biomass,
                                         rainfall,
                                         frac_available,
                                         bare_soil_infilt,
                                         infilt_saturation)
    assert(change_2 < change_1)


def test_soil_water_change_zero():
    #no surface water, no plants, no evaporation
    plant_biomass = 0
    soil_water = 3.0
    surface_water = 0
    frac_available = 0.1
    bare_soil_infilt = 0.15
    infilt_saturation = 5.
    plant_growth = 0.
    soil_water_evap = 0.
    uptake_saturation = 3.
    change = calc_soil_water_change(soil_water,
                                    surface_water,
                                    plant_biomass,
                                    frac_available,
                                    bare_soil_infilt,
                                    infilt_saturation,
                                    plant_growth,
                                    soil_water_evap,
                                    uptake_saturation)
    assert(change==0)
