USE QUANLYNHANSU;
GO

IF OBJECT_ID('dbo.department', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.department (
        deptno INT NOT NULL PRIMARY KEY,
        dname NVARCHAR(50) NOT NULL,
        loc NVARCHAR(50) NOT NULL
    );
END;
GO

IF OBJECT_ID('dbo.employee', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.employee (
        empno INT NOT NULL PRIMARY KEY,
        ename NVARCHAR(50) NOT NULL,
        job NVARCHAR(30) NOT NULL,
        mgr INT NULL,
        hiredate DATE NOT NULL,
        sal DECIMAL(12, 2) NOT NULL,
        comm DECIMAL(12, 2) NULL,
        deptno INT NOT NULL,
        CONSTRAINT FK_employee_department
            FOREIGN KEY (deptno) REFERENCES dbo.department(deptno)
    );
END;
GO

IF NOT EXISTS (SELECT 1 FROM dbo.department WHERE deptno = 10)
    INSERT INTO dbo.department (deptno, dname, loc)
    VALUES (10, N'ACCOUNTING', N'NEW YORK');

IF NOT EXISTS (SELECT 1 FROM dbo.department WHERE deptno = 20)
    INSERT INTO dbo.department (deptno, dname, loc)
    VALUES (20, N'RESEARCH', N'DALLAS');

IF NOT EXISTS (SELECT 1 FROM dbo.department WHERE deptno = 30)
    INSERT INTO dbo.department (deptno, dname, loc)
    VALUES (30, N'SALES', N'CHICAGO');

IF NOT EXISTS (SELECT 1 FROM dbo.department WHERE deptno = 40)
    INSERT INTO dbo.department (deptno, dname, loc)
    VALUES (40, N'OPERATIONS', N'BOSTON');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7839)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7839, N'KING', N'PRESIDENT', NULL, '1981-11-17', 5000, NULL, 10);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7566)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7566, N'JONES', N'MANAGER', 7839, '1981-04-02', 2975, NULL, 20);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7698)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7698, N'BLAKE', N'MANAGER', 7839, '1981-05-01', 2850, NULL, 30);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7782)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7782, N'CLARK', N'MANAGER', 7839, '1981-06-09', 2450, NULL, 10);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7788)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7788, N'SCOTT', N'ANALYST', 7566, '1982-12-09', 3000, NULL, 20);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7902)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7902, N'FORD', N'ANALYST', 7566, '1981-12-03', 3000, NULL, 20);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7369)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7369, N'SMITH', N'CLERK', 7902, '1980-12-17', 800, NULL, 20);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7499)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7499, N'ALLEN', N'SALESMAN', 7698, '1981-02-20', 1600, 300, 30);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7521)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7521, N'WARD', N'SALESMAN', 7698, '1981-02-22', 1250, 500, 30);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7654)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7654, N'MARTIN', N'SALESMAN', 7698, '1981-09-28', 1250, 1400, 30);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7844)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7844, N'TURNER', N'SALESMAN', 7698, '1981-09-08', 1500, 0, 30);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7876)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7876, N'ADAMS', N'CLERK', 7788, '1983-01-12', 1100, NULL, 20);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7900)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7900, N'JAMES', N'CLERK', 7698, '1981-12-03', 950, NULL, 30);

IF NOT EXISTS (SELECT 1 FROM dbo.employee WHERE empno = 7934)
    INSERT INTO dbo.employee (empno, ename, job, mgr, hiredate, sal, comm, deptno)
    VALUES (7934, N'MILLER', N'CLERK', 7782, '1982-01-23', 1300, NULL, 10);
GO

SELECT * FROM dbo.department ORDER BY deptno;
SELECT * FROM dbo.employee ORDER BY empno;
GO
