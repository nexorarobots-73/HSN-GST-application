def calculate_tax(base_value, slab):
    slab_map = {
        "0%": (0.0, 0.0),
        "0.25%": (0.125, 0.125),
        "3%": (1.5, 1.5),
        "5%": (2.5, 2.5),
        "12%": (6.0, 6.0),
        "18%": (9.0, 9.0),
        "28%": (14.0, 14.0)
    }
    cgst, sgst = slab_map.get(slab, (0.0, 0.0))
    return base_value * (cgst / 100), base_value * (sgst / 100)