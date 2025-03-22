from django.db import models

# Create your models here.


class DiemdanhRP(models.Model):
    lop = models.CharField(max_length=300, default= "", blank= True)
    monhoc = models.CharField(max_length=300, default= "", blank= True)
    thoigian = models.DateField()
    sv = models.CharField(max_length=300, default= "", blank= True)
    ghichu =models.CharField(max_length=300, default= "", blank= True)
    #sv = models.ForeignKey(Hssv, on_delete=models.RESTRICT)
    #lichhoc_id = models.IntegerField()

    def __str__(self):
        return self.sv

class Dashboard(models.Model):
    ma =models.CharField(max_length=300, default= "", blank= True)
    #sv = models.ForeignKey(Hssv, on_delete=models.RESTRICT)
    #lichhoc_id = models.IntegerField()

    def __str__(self):
        return self.ma

class Report(models.Model):
    ma =models.CharField(max_length=300, default= "", blank= True)
    #sv = models.ForeignKey(Hssv, on_delete=models.RESTRICT)
    #lichhoc_id = models.IntegerField()

    def __str__(self):
        return self.ma

class ChamcongRP(models.Model):
    ten = models.CharField(max_length=300, default= "", blank= True)
    monhoc = models.CharField(max_length=300, default= "", blank= True)
    lop = models.CharField(max_length=300, default= "", blank= True)
    thoigian = models.DateField()
    sogio = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.ten

class HocphiRP(models.Model):
    ten = models.CharField(max_length=300, default= "", blank= True)
    lop = models.CharField(max_length=300, default= "", blank= True)
    sotien = models.IntegerField()

    def __str__(self):
        return self.ten
