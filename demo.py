#coding: utf-8

import pytest
import allure

allure.environment(host="127.0.0.1")
allure.environment(platform="windows")
allure.environment(site="company")

@allure.feature("demo test")
class Test_demo:
	@allure.story("step_one")
	def test_one(self):
		allure.step('first')
		assert 1 == 2
		allure.step("secondly")
		assert 2 == 2

	@allure.story("step_two")
	def test_two(self):
		allure.step("third")
		assert 1 == 1	

	@allure.issue("https://www.baidu.com")
	def test_three(self):
		allure.step("four")
		assert 1 == 1	

@allure.feature("demo test 2")
class Test_demo_2:
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