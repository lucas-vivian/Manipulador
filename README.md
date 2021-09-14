# Trajectory Control with 5-DOF Manipulator

This repo contains the simulation and control algorithms of my undergraduate thesis project: [Five Degree of Freedom Manipulator Positioning Interface for Subsea Applications](https://www.maxwell.vrac.puc-rio.br/colecao.php?strSecao=resultado&nrSeq=53802@2), which uses the ARM 5E Mini manipulator from ECA Robotics.

It's composed by three folders:

- Matlab: Theoretical simulations of the manipulator's kinematic model;
- Python: Trajectory control and data send/receive algorithms to/from the manipulator;
- Trajectory Points: Set of points of three different trajectories to be coursed by the manipulator.

## Matlab

This folder is divided in Forward and Inverse Kinematics. The FK folder contains four main simulation files: **FK_TCC**, **FK_Workspace**, **Workspace_TCC** and **DH_Robot_literal**. There's a support file called **MGD_DH** for the last one. The IK folder has only one main file **minsumsquare_test.m** and one support file.

### Forward Kinematics (FK)

The forward kinematics problem is defined by: ".. determine the position n and orientation of the end effector in terms of joint variables". Using the Denavit-Hartenberg notation, the description of this problem in multiple DOF is simplified.

#### 1. Interactive FK interface with `FK_TCC.m`

Having determined the DH parameters and the offset of the manipulator, the links are created and the joint limits defined. Using the _teach_ function from Peter Corke toolbox we create an interactive enviroment to solve the forward kinematics problem of the manipulator.

When the program is executed, a new window will appear allowing the user to set angles for each joint showing the three coordinates of the end-effector as result.

#### 2. Generating workspace with `Workspace_TCC.m`

The workspace of a manipulator is defined by all the points that the end-effector can reach without going over the manipulator's mechanical limits. Knowing the joint limits and using the ***linspace*** function, we create a aproximation of all joints' possible values to generate the workspace points through the forward kinematics equations.

Instead of using a ***for*** loop to apply each set of angles to each joint individually, we can use the ***ndgrid*** function to create a 50x50x50 matrix to each set to then use directly into the equations and then scatter the results.

#### 3. Combining interface with workspace in `FK_Workspace.m`

Combining the two previous files we get a validation to the equations because it's possible to observe that when sliding the joints, they doesn't exceed workspace plot.

#### 4. Generating Forward Kinematics equations in `DH_Robot_literal.m`

### Inverse Kinematics (IK)

## Python
 
## Pontos

