#---------------------author: hfxu.oth 2018-04-05
#---------------------revision: 0.0.8 
#---------------------code: utf-8

--备份数据库路径
DECLARE @backFolder VARCHAR(5000)

--备份数据库的时间
DECLARE @backTime VARCHAR(200)

--拼sql执行的语句
DECLARE @sql NVARCHAR(max)

SET @backFolder = '{{devopsBackupPath}}'
SET @backTime = '{{devopsBackuptime}}'
SET @sql = N'BACKUP DATABASE [{{dbName}}] TO DISK = N'''+@backFolder+'{{dbName}}'+@backTime+'.bak'' WITH NOFORMAT, NOINIT, NAME= N''{dbName}}-完整数据库备份'', SKIP, NOREWIND, NOUNLOAD, STATS = 10'
EXEC (@sql)
