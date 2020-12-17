#! /bin/bash
mvn compile
mvn exec:java -Dexec.mainClass="MainApp" -Dexec.args="$*"
