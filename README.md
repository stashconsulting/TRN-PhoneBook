# Traning of Application Cycle 

## Table of Contents

* Introduction
* API project
* What we have achieved
* Usage
* Authenticate gcloud

## Introduction

This project is part of the training process of our new employees at Fiveops Solutions, with the purpose of giving a brief summary of the application cycle and get a quick start with Docker, MySQL, Gcloud and others. 

## API project

We have created a simple Rest API on python using Flask-restful, this Api emulates a minimal phone registry saving and migrating data from mysql. Using Gcloud we were available to build and deploy a container from the Pipeline.

 ## What we have achieved
 
We created a Rest Api of a phone registry that receive requests through HTTP, where you can register users information, look up fully/partially, edit, delete and storage their information. 

We have migrate database through mysql where all the users information are save automatically. 

We have connected the API with Gcloud Run to build and deploy the app on a container from the Pipeline.

## Authenticate gcloud

Prior to running, ensure you have authenticated your gcloud client by running the following command:

gcloud auth application-default login

## Usage

export mysql_host=****
export mysql_user=****
export mysql_password=****
export mysql_port=****
export api_port=****
export socket=""

### Contact

Mellanie Acevedo - @macvdos - stashconsulting
Pending review by - @sjortiz - stashconsulting
