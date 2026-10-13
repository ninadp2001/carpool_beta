# Car Pool v1 (2022, legacy)

Original Semester 5 project: plain PHP + MySQL on XAMPP, with a car rental flow,
a car wash booking flow, a dummy card payment page and a dompdf invoice.

Kept here for history only. It has known issues that the rewrite fixes:
SQL built from raw `$_POST` values (SQL injection), plain-text passwords,
prices calculated in the browser and trusted by the server, and a rental insert
that doesn't match the `rentalbooking` table.

`register.sql` has been scrubbed of real user data. To run it: import it into
MySQL as database `register`, put the folder in `htdocs`, and run `composer require dompdf/dompdf`.
