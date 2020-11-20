# -*- coding: utf-8 -*-
"""ppgr_domaci_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Qi3VkpqiWDG2lpRP6OjwlvljX7KYykb0
"""

import numpy as np
from numpy import linalg as LA
import math

'''
  Funkcija koja vrsi noriranje datog vektora
'''

def normiraj(p):
  norm_ = math.sqrt(p[0]**2 + p[1]**2 + p[2]**2)
  return p/norm_

def norma(p):
  return math.sqrt(p[0]**2 + p[1]**2 + p[2]**2)

'''
  Funkcija prima matricu A koja je ortoganalna i vazi det(A) = 1
  i vraca jedinicni vektor p i ugao fi iz [0, pi] takav da vazi
  da je matrica A matrica rotacije oko prave p za ugao fi
'''
def AxisAngle(A):
  if round(LA.det(A)) != 1:
    print("Determinanta matrice A je razlicita od 1!")
    return
  '''
  TODO
  if A @ A.T == np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
    print("Matrica nije ortogonalna!")
    return
  '''

  first = A[0]
  second = A[1]
  p = np.cross(first, second)
  p = normiraj(p) # Trazeni jedinicni vektor p
  
  u = first # Vektor u je normalan na vektor p 

  u_bar = A @ u

  fi = math.acos((u @ u_bar.T)/(norma(u)*norma(u_bar)))

  mesoviti = LA.det(np.array([u, u_bar, p]))
  if(mesoviti < 0):
    p = -p
    fi = 2*math.pi - fi

  return (p, fi)


p, fi = AxisAngle(np.array([[1/9, 8/9, -4/9], [-4/9, 4/9, 7/9], [8/9, 1/9, 4/9]]))
print(f"Jedinicni vektor oko kog se rotira: {p}")
print(f"Ugao za koji se rotira: {fi}")

def izmnozi(p):
  p_t = np.array([[p[0]], [p[1]], [p[2]]])
  return np.array([p_t[0]*p, p_t[1]*p, p_t[2]*p])
'''
  Funkcija koja racuna matricu rotacije oko prave p za ugao fi
  Kao ulaz prima vektor kolonu oko kog se vrsi rotacija i ugao rotacije
'''

def Rodrigez(p, phi):
  p = normiraj(p)
  E = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
  p_pt = izmnozi(p)
  p_x = np.array([[0, -p[2], p[1]], [p[2], 0, -p[0]], [-p[1], p[0], 0]])

  return p_pt + math.cos(phi)*(E - p_pt) + math.sin(phi)*p_x

Rodrigez(np.array([1, 0, 0]), math.pi/2)

'''
  Funkcija prima ortogonalnu matricu A i vazi det(A) = 1
  i vraca Ojlerove uglove phi, tetha, psi redom
'''
def A2Euler(A):
  if round(LA.det(A)) != 1:
    print("Determinanta matrice A je razlicita od 1!")
    return
  '''
  TODO
  if A @ A.T == np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
    print("Matrica nije ortogonalna!")
    return
  '''

  if (A[2][0] < 1 and A[2][0] > -1):
    psi = math.atan2(A[1][0], A[0][0])
    tetha = math.asin(-A[2][0])
    phi = math.atan2(A[2][1], A[1][1])
    return phi, tetha, psi

  if (A[2][0] == -1):
    phi = 0
    tetha = math.pi/2
    psi = math.atan2(-A[0][1], A[1][1])
    return phi, tetha, psi

  phi = 0
  tetha = -math.pi/2
  psi = math.atan2(-A[0][1], A[1][1])
  return phi, tetha, psi

phi, tetha, psi = A2Euler(np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]]))
print("Uglovi:")
print(f"Psi: {psi}")
print(f"Tetha: {tetha}")
print(f"Phi: {phi}")

def Euler2A(phi, tetha, psi):
  Rx_phi = Rodrigez(np.array([1, 0, 0]), phi)
  Ry_tetha = Rodrigez(np.array([0, 1, 0]), tetha)
  Rz_psi = Rodrigez(np.array([0, 0, 1]), psi)

  return Rz_psi @ Ry_tetha @ Rx_phi

A = Euler2A(-math.asin(1/4), -math.asin(8/9), math.atan(4))
print(A)