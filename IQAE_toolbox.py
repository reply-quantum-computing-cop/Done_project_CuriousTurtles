from pennylane import numpy as np
import pennylane as qml
import pickle
from scipy.linalg import eigh



def angstrom_to_bohr(dist):
    return dist*1.88973


##############          CLEAN FUNCTION         ##############
qubits_tap = 7
def expectation_obs(psi0,Pi,Pj,H=qml.Hamiltonian(coeffs=[1], observables=[qml.Identity(wires=range(qubits_tap))] )):
    """Computes the expectation value of a Hamiltonian sandwiched between two Pauli words.
    """
    Pwi = qml.pauli.PauliWord(dict(zip(list(range(len(Pi))), Pi)))
    Pwj = qml.pauli.PauliWord(dict(zip(list(range(len(Pj))), Pj)))
    
    Psi = qml.pauli.PauliSentence({Pwi: 1.})
    Psj = qml.pauli.PauliSentence({Pwj: 1.})
    PsH = qml.pauli.pauli_sentence(H)

    Pi_H_Pj = Psi*PsH*Psj
    
    # BUG TO BE REPORTED : 
    # ps.Hamlitonian does not work in case ps contains complex coefficients: 
    # reproducer
    # pw1 = qml.pauli.PauliWord({0:"X"})
    # Psi = qml.pauli.PauliSentence({pw1: 1.,pw1: 1.2j})
    # Psi.hamiltonian()

    coeffs,ops = zip(*[ (coeff, pw.hamiltonian(wire_order=list(H.wires)).ops[0])  for pw, coeff in Pi_H_Pj.items()])

    #coeffs,ops = zip(*[ (coeff, pw.operation(wire_order=list(H_tapered.wires)))  for pw, coeff in Pi_H_Pj.items()])
    #obs_groupings, coeffs_groupings = qml.pauli.group_observables(ops, coeffs, 'qwc', 'rlf')
    #Pi_H_Pj = qml.Hamiltonian(coeffs = coeffs_groupings,
    #                            observables = obs_groupings)
    dev = qml.device("default.qubit", wires=qubits_tap)
    @qml.qnode(dev)
    def circ():
        Pi_H_Pj = qml.Hamiltonian( coeffs = coeffs,
                                observables = ops,
                                simplify=False
                            )
        qml.QubitStateVector(psi0, range(qubits_tap))
        return qml.expval(Pi_H_Pj)
    
    
    return circ()



##############          LESS CLEAN FUNCTIONS (that work)         ##############
#
#    These functions have been refactored above using PauliWords and PauliSentences. However some bugs retained us from using them
#     
#   BUG TO BE REPORTED : 
#       Description:
#           ps.Hamlitonian does not work in case ps contains complex coefficients: 
#       Reproducer:
#           pw1 = qml.pauli.PauliWord({0:"X"})
#           Psi = qml.pauli.PauliSentence({pw1: 1.,pw1: 1.2j})
#           Psi.hamiltonian()
#   
#   A more sever bug is on the calculation of the matrix elements of D
#   Both functions above and in the notebook provide the exact same Hamiltonian product with the Pauli words
#   Discrepencies on the expectation value calculations whether the grouping_method 'qwc' is called or not.
#   To reproduce it:
#
#
#
##############


# Multiplication rule for two Pauli matrices
def multiply(s1, s2):
    if s1=='I':
        return 0, s2
    if s2=='I':
        return 0, s1
    if s1==s2:
        return 0,'I'
    else:
        
        if s1=='X':
            if s2=='Y':
                return 1, 'Z' #XY = iZ
            else:
                return 3, 'Y' #XZ = -iY
        elif s1=='Y':
            if s2=='X':
                return 3, 'Z' #YX = -iZ
            else:
                return 1, 'X' #YZ = iX
        else:
            if s2=='X':
                return 1, 'Y' #ZX = iY
            else:
                return 3, 'X' #ZY = -iX
                

# Multiply two Pauli words and keep track of the phase
def P_multiply(P1,P2):
    #if len(P1)!=len(P2):
    #    raise Exception("Pauli words must have the same length")
        
    Phase = 0
    P = ''
    for i in range(len(P1)):
        phase, s = multiply(P1[i], P2[i])
        Phase += phase
        P += s
    return Phase%4, P
    

# Multiply three Pauli words and keep track of the phasdef Ps_multiply(P1,P2,P3):
def Ps_multiply(P1,P2,P3):
    #print(P1,P2,P3)
    phase_, P_ = P_multiply(P1,P2)
    phase, P = P_multiply(P_,P3)
    return (phase_+phase)%4, P




##############          TOOLBOX FOR GENERATING THE KRYLOV-INSPIRED SUBSPACE         ##############

# Return the Pauli words of H in string form
def extract_basis_str(H,wire_map):
    
    N = len(H.coeffs)
    basis_str = set()
    for i in range(N):
        basis_str.add( qml.pauli.pauli_word_to_string(H.ops[i],wire_map) )
        
    return basis_str


# Generate the cumulative space CSK
def cumulative_space(H,wire_map,K):
    a = set()
    if K==0:
        return [{'I'*qubits_tap}]
    
    else:
        CS1 = extract_basis_str(H,wire_map)
        
        Id = 'I'
        for i in range(qubits_tap-1):
            Id += 'I'
            
        basis = [{'I'*qubits_tap},CS1]
        for k in range(K-1):
            a.update(basis[-2])
            basis.append(  increment_cumulative_space( basis[-1].difference(a)  ,CS1)   )
        a.update(*basis[-2:])
    return a


# Help generate the cumulative space
def increment_cumulative_space(basis, CS1):
    SK = set()
        
    for element in basis:
        for gen in CS1:
            _, P = P_multiply(element, gen)
            SK.add(P)
    return SK