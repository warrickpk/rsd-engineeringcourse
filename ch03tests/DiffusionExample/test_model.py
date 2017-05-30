from MonteCarlo import MonteCarlo
from nose.tools import assert_equal
from nose.tools import assert_equal, assert_almost_equal, assert_true, assert_raises
from mock import MagicMock


def test_input_sanity():
    """ Check incorrect input do fail """
    energy = MagicMock()
    
    with assert_raises(NotImplementedError) as exception: 
        MonteCarlo(sum, [1, 1, 1], 0e0)
    with assert_raises(ValueError) as exception: 
        MonteCarlo(energy, [1, 1, 1], temperature=-1e0)
        
    with assert_raises(TypeError) as exception: 
        MonteCarlo(energy, [1.0, 2, 3])
    with assert_raises(ValueError) as exception: 
        MonteCarlo(energy, [-1, 2, 3])
    with assert_raises(ValueError) as exception: 
        MonteCarlo(energy, [[1, 2, 3], [3, 4, 5]])
    with assert_raises(ValueError) as exception: 
        MonteCarlo(energy, [3])
    with assert_raises(ValueError) as exception: 
        MonteCarlo(energy, [0, 0])
    
    
    
def test_move_particle_one_over():
    """ Check density is change by a particle hopping left or right. """
    from numpy import nonzero, multiply
    from numpy.random import randint
    
    energy = MagicMock()
    
    for i in range(100): 
        # Do this n times, to avoid 
        # issues with random numbers
        # Create density
        
        density = randint(50, size=randint(2, 6))
        mc = MonteCarlo(energy, density)
        # Change it
        new_density = mc.change_density(density)

        # Make sure any movement is by one
        indices = nonzero(density - new_density)[0]
        assert_equal(len(indices), 2, "densities differ in two places")
        assert_equal( 
            multiply.reduce((density - new_density)[indices]), 
            -1,
            "densities differ by + and - 1"
        )
        
        
def test_equal_probability():
    """ Check particles have equal probability of movement. """
    from numpy import array, sqrt, count_nonzero
    
    energy = MagicMock()
    
    density = array([1, 0, 99])
    mc = MonteCarlo(energy, density)
    changes_at_zero = [
        (density - mc.change_density(density))[0] != 0 for i in range(10000)]
    assert_almost_equal(
        count_nonzero(changes_at_zero), 
        0.01 * len(changes_at_zero), 
        delta = 0.5 * sqrt(len(changes_at_zero))
    )
    
def test_accept_change():
    """ Check that move is accepted if second energy is lower """
    from numpy import sqrt, count_nonzero, exp
    
    energy = MagicMock
    mc = MonteCarlo(energy, [1, 1, 1], temperature=100.0)
    # Should always be true. 
    # But do more than one draw, 
    # in case randomness incorrectly crept into
    # implementation
    for i in range(10):
        assert_true(mc.accept_change(0.5, 0.4))
        assert_true(mc.accept_change(0.5, 0.5))

    # This should be accepted only part of the time, 
    # depending on exponential distribution
    prior, successor = 0.4, 0.5
    accepted = [mc.accept_change(prior, successor) for i in range(10000)]
    assert_almost_equal( 
        count_nonzero(accepted) / float(len(accepted)),
        exp(-(successor - prior) / mc.temperature),
        delta = 3e0 / sqrt(len(accepted))
    )

    

def test_main_algorithm():
    import numpy as np
    from numpy import testing
    from mock import Mock
    
    density = [1, 1, 1, 1, 1]
    energy = MagicMock()
    mc = MonteCarlo(energy, density, itermax = 5)
    
    acceptance = [True, True, True, True, True]
    mc.accept_change = Mock(side_effect = acceptance)
    mc.random_agent = Mock(side_effect = [0, 1, 2, 3, 4])
    mc.random_direction = Mock(side_effect = [1, 1, 1, 1, -1])
    np.testing.assert_equal(mc.step()[1], [0,1,1,2,1])

    
    