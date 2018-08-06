#! /usr/bin/env python3

import mpl_toolkits
import matplotlib.pyplot as plt
import uszipcode


def pop_map(zipcode='94025'):
    search = uszipcode.ZipcodeSearchEngine()
    print(search.all_state_short)
    print(search.by_zipcode('94025'))


if __name__ == '__main__':
    pop_map()
