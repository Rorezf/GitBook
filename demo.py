#coding: utf-8

import pytest
import allure

allure.environment(host="127.0.0.1")
allure.environment(browser="chrome")

@allure.feature("demo test")
class Test_demo:
	@allure.story("step_one")
	def test_one(self):
		# with allure.step("first"):
		# 	allure.attach("login")
		# 	allure.attach("click")
		# with allure.step("secondly"):
		# 	allure.attach("expect:1")
		allure.step('first')
		assert 1 == 1
		allure.step("secondly")
		assert 2 == 2

	def test_two(self):
		assert 1 == 1	