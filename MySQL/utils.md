# Utils

## Insert if not exist

```sql
INSERT INTO casa_bugzilla.bugs (
	bug_id, short_desc, bug_status, bug_level, updateTime
) SELECT
	{}, '', '', '', '{}'
FROM DUAL
WHERE
	NOT EXISTS (
		SELECT bug_id
		FROM casa_bugzilla.bugs
		WHERE bug_id ={} );

INSERT INTO testlink_history.user_assignments SELECT a.*
FROM user_assignments a
LEFT JOIN testplan_tcversions b ON a.feature_id = b.id
WHERE b.tcversion_id = {}
AND NOT EXISTS (
	SELECT a.id
	FROM testlink_history.user_assignments a
	LEFT JOIN testlink_history.testplan_tcversions b 
	ON a.feature_id = b.id
	WHERE b.tcversion_id = {} );
```

## Count

```sql
SELECT
	COALESCE (STATUS, 'all'),
	count(*)
FROM
	allure_report_info
WHERE
	projectName = '{}'
AND buildId = '{}'
GROUP BY
	STATUS WITH ROLLUP;
```

## Union

```sql
(
	SELECT
		a.testproject_id, b. NAME
	FROM
		bug_mgmt_view a
	LEFT JOIN nodes_hierarchy b ON a.testproject_id = b.id
	LEFT JOIN user_department c on a.user_id=c.id
	WHERE
		c.department='{}' AND a.active={}
	AND a.updateTime BETWEEN '{}' AND '{}'
	GROUP BY
		a.testproject_id
) UNION (
	SELECT
		a.testproject_id,
		b. NAME
	FROM
		casa_bugzilla.bugs_external_view a
	LEFT JOIN nodes_hierarchy b ON a.testproject_id = b.id
	LEFT JOIN user_department c on a.user_id = c.id
	WHERE
		c.department='{}' AND a.active={}
	AND a.updateTime BETWEEN '{}' AND '{}'
	GROUP BY
		a.testproject_id
	);
```

## Same Field

```sql
SELECT
	id, creation_ts
FROM
	testplan_tcversions_copy t1
INNER JOIN (
	SELECT
		testplan_id,
		tcversion_id,
		platform_id
	FROM
		testplan_tcversions_copy
	GROUP BY
		testplan_id,
		tcversion_id,
		platform_id
	HAVING
		count(1) > 1
) t2 ON t1.testplan_id = t2.testplan_id
AND t1.tcversion_id = t2.tcversion_id
AND t1.platform_id = t2.platform_id;
```

```sql
SELECT
	group_concat(id ORDER BY creation_ts)
FROM
	testplan_tcversions
GROUP BY
	testplan_id,
	tcversion_id,
	platform_id
HAVING
	count(1) > 1;
```