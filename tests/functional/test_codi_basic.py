''' Test CODI RESTful API '''

import unittest
import subprocess
import sys
import inspect
import time
from codi import codiDB
from utils.globs import config

class CropsBasicTests(unittest.TestCase):
    ''' Base class for testing codi '''

    def setUp(self):
        ''' Define some unique data for validation '''
        self.codiAddr = "127.0.0.1"
        self.codiPort = "10000"
        self.image = "crops/chameleonsocks"
        codiDB.CodiDB(config.CODI_DB)

    def tearDown(self):
        ''' Destroy unique data '''

    def test_1_start_codi(self):
        ''' Start codi'''
        success=True
        try:
            p = subprocess.Popen(["gunicorn", "-w", "4", "-t", "180","-b", self.codiAddr + ":" + self.codiPort, "launchers.codi-launcher:app"],stdout=subprocess.PIPE)
            time.sleep(2)
        except subprocess.CalledProcessError as e:
            print(e.output)
            self.assertTrue(false)
        self.assertTrue(success)

    def test_2_list_api(self):
        ''' List codi API'''
        cmd = "curl --silent -o- http://%s:%s/codi/ "%(self.codiAddr,self.codiPort)
        try:
            p=subprocess.Popen(cmd.split(), stderr=sys.stderr, stdout=subprocess.PIPE, shell=False)
        except subprocess.CalledProcessError as e:
            print(e.output)
            self.assertTrue(False)

        upString="Show CODI API"
        found = False
        output=p.communicate()[0]
        output = output.decode()
        for line in output.split('\n'):
            if line.find(upString) >= 0:
                found=True
                break

        if not found:
            print("%s did not appear in check %s\n"%(upString, inspect.stack()[0][3]))
        self.assertTrue(found)

    def test_3_register_toolchain(self):
        ''' Register toolchain '''
        SUBSTRING="Registration failed"
        try:
            p = subprocess.Popen(["python3","-m", "launchers.turff-launcher", "--ip", "127.0.0.1", "--port", "10000"],stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(e.output)
            self.assertTrue(False)

        failure=False
        output=p.communicate()[0]
        output = output.decode()
        print(output)

        for line in output.split('\n'):
            if line.find(SUBSTRING) >= 0:
                failure=True
                break
        self.assertTrue(not failure)

    def test_4_list_toolchains(self):
        cmd = "curl --silent -o- http://%s:%s/codi/list-toolchains"%(self.codiAddr,self.codiPort)
        try:
            p=subprocess.Popen(cmd.split(), stderr=sys.stderr, stdout=subprocess.PIPE, shell=False)
        except subprocess.CalledProcessError as e:
            print(e.output)
            self.assertTrue(False)

        FOUNDSTRING="i586-poky-linux-"
        found = False
        output=p.communicate()[0]
        output = output.decode()
        for line in output.split('\n'):
            if line.find(FOUNDSTRING) >= 0:
                found=True
                break

        if not found:
            print("%s did not appear in check %s\n"%(FOUNDSTRING, inspect.stack()[0][3]))
        self.assertTrue(found)

    def test_5_find_image(self):
        cmd = "curl --silent -o- http://%s:%s/codi/find-image?image=%s"%(self.codiAddr,self.codiPort, self.image)
        try:
            p=subprocess.Popen(cmd.split(), stderr=sys.stderr, stdout=subprocess.PIPE, shell=False)
        except subprocess.CalledProcessError as e:
            print(e.output)
            self.assertTrue(False)

        FOUNDSTRING="chameleonsocks"
        found = False
        output=p.communicate()[0]
        output = output.decode()
        for line in output.split('\n'):
            if line.find(FOUNDSTRING) >= 0:
                found=True
                break

        if not found:
            print("%s did not appear in check %s\n"%(FOUNDSTRING, inspect.stack()[0][3]))
        self.assertTrue(found)

    def test_6_pull_image(self):
        cmd = "curl --silent -o- http://%s:%s/codi/pull-image?image=%s"%(self.codiAddr,self.codiPort, self.image + ":latest")
        try:
            subprocess.call(cmd.split(), stderr=sys.stderr, stdout=subprocess.PIPE, shell=False)
            p=subprocess.Popen(["docker", "images"], stderr=sys.stderr, stdout=subprocess.PIPE, shell=False)
        except subprocess.CalledProcessError as e:
            print(e.output)
            self.assertTrue(False)

        FOUNDSTRING=self.image
        found = False
        output=p.communicate()[0]
        output = output.decode()
        for line in output.split('\n'):
            if line.find(FOUNDSTRING) >= 0:
                found=True
                break

        if not found:
            print("%s did not appear in check %s\n"%(FOUNDSTRING, inspect.stack()[0][3]))
        self.assertTrue(found)

    def test_7_remove_image(self):
        cmd = "curl --silent -o- http://%s:%s/codi/remove-image?image=%s"%(self.codiAddr,self.codiPort, self.image + ":latest")
        try:
            subprocess.call(cmd.split(), stderr=sys.stderr, stdout=subprocess.PIPE, shell=False)
            p=subprocess.Popen(["docker", "images"], stderr=sys.stderr, stdout=subprocess.PIPE, shell=False)
        except subprocess.CalledProcessError as e:
            print(e.output)
            self.assertTrue(False)

        FOUNDSTRING=self.image
        found = False
        output=p.communicate()[0]
        output = output.decode()
        for line in output.split('\n'):
            if line.find(FOUNDSTRING) >= 0:
                found=True
                break

        self.assertFalse(found)
