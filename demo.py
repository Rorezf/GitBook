#coding: utf-8

import pytest
import allure

allure.environment(platform="windows")
allure.environment(summary="http://192.168.55.192:8888/summary")

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

	@allure.issue("http://192.168.55.192:8888/index/?stepName=@1.1:%20show%20ldp")
	def test_three(self):
		allure.step("four")
		assert 1 == 12

@allure.feature("demo test 2")
@allure.testcase("http://192.168.55.192:8888/index/?stepName=@8.0.0: preconfiguration&caseName=Tests.smoke.aaa.aaa_radius.test&projectName=19-dxiaoming-autoapp")
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