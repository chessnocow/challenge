# SQL task

The below database table schema captures the historical state for every change a user makes to their profile. The current user profile can be found in the record with the latest created timestamp for any given user_id.

__Table: user_changes__

| __Column__ | __Description__ |
|------------|-----------------|
| uuid          |String: The unique record id                 |
| user_id       |String: The unique id of the user                 |
| user_created  |Timestamp: When the user was created                 |
| created          |Timestamp: When this record was created                 |
| name          |String: The full name of the user                 |
| email           |String: The email address of the user                 |

## Q1. Write an SQL query using vendor neutral ANSI SQL to find the user_id, current name and current email address for all users. Do not worry too much about the performance of the query, favour readability.

```
SELECT
  UC1.user_id,
  UC1.name,
  UC1.email
FROM
  user_changes AS UC1
  LEFT JOIN user_changes AS UC2 ON (
    UC1.user_id = UC2.user_id
    AND UC1.created < UC2.created
  )
WHERE
  UC2.created IS NULL
ORDER BY
  UWI;
```

## Q2. Write an SQL query using vendor neutral ANSI SQL to find the median time between the second and third profile edit. Do not worry too much about the performance of the query, favour readability.

```
WITH
  # Table with the sequence number of the change
  TABLE_WITH_NUMBER AS (
    SELECT
      *,
      ROW_NUMBER() OVER (
        PARTITION BY
          user_id
        ORDER BY
          created ASC
      ) AS CHANGE_N
    FROM
      user_changes
    ORDER BY
      user_id,
      CHANGE_N
  ),
  # Table of second edits
  SECOND_EDIT AS (
    SELECT
      *
    FROM
      TABLE_WITH_NUMBER
    WHERE
      CHANGE_N = 3
  ),
  # Table of third edits
  THIRD_EDIT AS (
    SELECT
      *
    FROM
      TABLE_WITH_NUMBER
    WHERE
      CHANGE_N = 4
  ),
  # Differences between third and second edits joined on user_id
  TIMEDIF AS (
    SELECT
      datediff(
        to_timestamp(THIRD_EDIT.created),
        to_timestamp(SECOND_EDIT.created)
      ) AS DIF
    FROM
      SECOND_EDIT
      JOIN THIRD_EDIT ON SECOND_EDIT.user_id = THIRD_EDIT.user_id
    ORDER BY
      DIF
  )
# Calculate median. If number of rows is odd then middle element will be in both parts
SELECT
(
 (SELECT MAX(DIF) FROM
   (SELECT TOP 50 PERCENT DIF FROM TIMEDIF ORDER BY DIF) AS BottomHalf)
 +
 (SELECT MIN(DIF) FROM
   (SELECT TOP 50 PERCENT DIF FROM TIMEDIF ORDER BY DIF DESC) AS TopHalf)
) / 2 AS TIMEDIF_MEDIAN ;

```