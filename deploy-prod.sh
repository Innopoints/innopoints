#!/bin/bash
cd ${PROJECT_HOME} && docker-compose -f docker-compose.prod.yaml up --build
