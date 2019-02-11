"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies_generated = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0,None,0.0,0.0)]
        
        
    def __str__(self):
        
        """
        Return human readable state
        """
        output = "\ntotal_cookies_generated = " + str(self._total_cookies_generated) + "\n"
        output += "current_cookies         = " + str(self._current_cookies) + "\n"
        output += "current_time = " + str(self._current_time) + "\n"
        output += "current_cps = " + str(self._current_cps)
        
        return output
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        cookies_needed = cookies - self._current_cookies
        if cookies_needed <= 0:
            return 0.0
        else:
            #print math.floor((cookies_needed / self.current_cps) + 0.5)
            return math.ceil((cookies_needed / self._current_cps))
        
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time <= 0:
            return
        else:
            cookies_generated = time * self._current_cps
            self._total_cookies_generated += cookies_generated
            self._current_cookies += cookies_generated
            self._current_time += time
            
    
    def buy_item(self, item_name, cost, additional_cps):
        
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time,item_name,cost,self._total_cookies_generated))
            return True
        return False  
            
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    # Replace with your code
    buildinfo_clone = build_info.clone()
    click_state = ClickerState()
    while(True):
        time_left = duration - click_state.get_time()
        if (time_left < 0):
            break
        build_item = strategy(click_state.get_cookies(), click_state.get_cps(),time_left, buildinfo_clone)        
        if (build_item == None):
            break
        else:
            time_to_wait = click_state.time_until(buildinfo_clone.get_cost(build_item))
            if time_to_wait > time_left:
                break
            click_state.wait(time_to_wait)
            click_state.buy_item(build_item,buildinfo_clone.get_cost(build_item),buildinfo_clone.get_cps(build_item))
            buildinfo_clone.update_item(build_item)
            #else:
            #    click_state.wait(time_to_wait)
            #    click_state.buy_item(build_item,buildinfo_clone.get_cost(build_item),buildinfo_clone.get_cps(build_item))
            #    buildinfo_clone.update_item(build_item)
    
    time_left = duration - click_state.get_time()
    if (time_left > 0):
        click_state.wait(time_left)

    #if(click_state.buy_item(build_item,buildinfo_clone.get_cost(build_item),buildinfo_clone.get_cps(build_item))):
    #    buildinfo_clone.update_item(build_item)
        
    return click_state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    This is a cheap strategy
    """
    build_items = build_info.build_items()
    total_cookies = cookies + (cps*time_left)
    #print build_items
    cheap_item = build_items[0]
    cheap_cost = build_info.get_cost(cheap_item)
    for item in build_items:
        if (build_info.get_cost(item) < cheap_cost):
            cheap_cost = build_info.get_cost(item)
            cheap_item = item
    if (cheap_cost <= total_cookies):
        #print cheap_item
        return cheap_item

    return None

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    This is expensive strategy
    """
    
    build_items = build_info.build_items()
    total_cookies = cookies + (cps*time_left)
    while (len(build_items) > 0):
        exp_item = build_items[0]
        exp_cost = build_info.get_cost(build_items[0])
        for item in build_items:
            if (build_info.get_cost(item) > exp_cost):
                exp_cost = build_info.get_cost(item)
                exp_item = item
    
        if (exp_cost <= total_cookies):
            return exp_item
        else:
            build_items.remove(exp_item)
    
    return None

def strategy_best(cookies, cps, time_left, build_info):
    """
    This is the best strategy
    """
    
    build_items = build_info.build_items()
    total_cookies = cookies + (cps*time_left)
    while (len(build_items) > 0):
        best_item = build_items[0]
        best_cps = build_info.get_cps(best_item)
        best_cost = build_info.get_cost(best_item)
        best_ratio = best_cps/best_cost
        for item in build_items:
            item_ratio = build_info.get_cps(item)/build_info.get_cost(item)
            if (item_ratio > best_ratio):
                best_cps = build_info.get_cps(item)
                best_item = item
                best_cost = build_info.get_cost(item)
            
        if (best_cost <= total_cookies):
            #print best_item
            return best_item
        else:
            build_items.remove(best_item)
    
    return None

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

