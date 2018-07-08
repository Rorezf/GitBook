#coding: utf-8

import pytest
import allure

allure.environment(host="127.0.0.1")
allure.environment(browser="chrome")

@allure.feature("demo test")
class Test_demo:
	@allure.story("step_one")
	def test_one(self):
		allure.step('first')
		assert 1 == 1
		allure.step("secondly")
		assert 2 == 3

	@allure.story("step_two")
	def test_two(self):
		allure.step("third")
		assert 1 == 1	

@allure.feature("demo test 2")
class Test_demo_2:
	@allure.story("step_one")
	def test_one(self):
		allure.step('first')
		assert 1 == 1
		allure.step("secondly")
		assert 2 == 2

	@allure.story("step_two")
	def test_two(self):
		allure.step("third")
		assert 1 == 4	