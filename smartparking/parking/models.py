from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext as _


class Unity(TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name= _('Nome'))
    location = models.CharField(blank=True, null=True, max_length=500, verbose_name= _('Localidade'))
    phone = models.CharField(blank=True, null=True, max_length=15, verbose_name= _('Telefone'))
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')

    class Meta:        
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.name


class Space(TimeStampedModel):
    TYPE = [
        ( 1, _("Normal")),
        ( 2, _("Preferencial")),        
    ]

    STATUS = [
        ( 1, _("Livre")),
        ( 2, _("Ocupada")),        
    ]

    code = models.CharField(max_length=10, verbose_name= _('Código'))
    sector = models.CharField(max_length=10, verbose_name= _('Setor'))
    type = models.IntegerField(choices=TYPE, default=1, verbose_name=_('Tipo'))
    status = models.IntegerField(choices=STATUS, default=1, verbose_name=_('Situação'))
    unity = models.ForeignKey(Unity,on_delete=models.CASCADE, verbose_name= _('Unidade'))
    
    class Meta:        
        verbose_name = 'Vaga'
        verbose_name_plural = 'Vagas'

    def __str__(self):
        return '{}-{}'.format(self.code, self.sector)

class SpaceEvent(TimeStampedModel):
    TYPE = [
        ( 1, _("Livre")),
        ( 2, _("Ocupado")),        
    ]

    space = models.ForeignKey(Space,on_delete=models.CASCADE, verbose_name= _('Vaga'))    
    event_date = models.DateTimeField(verbose_name= _('Data/Hora'))
    type = models.IntegerField(choices=TYPE, default=1, verbose_name=_('Tipo'))
    
    class Meta:        
        verbose_name = 'Vaga - Evento'
        verbose_name_plural = 'Vaga - Eventos'

    def __str__(self):
        return self.space.code

    def save(self, *args, **kwargs):
        """
        Update the space status.
        """
        try:
            space = Space.objects.get(id=self.space.id)
            space.status = self.type
            space.save()
            space.commit()
            
        except: pass
        super(SpaceEvent, self).save(*args, **kwargs)


class OCRCamera(TimeStampedModel):
    code = models.CharField(max_length=10, verbose_name= _('Código'))
    location = models.CharField(max_length=50, verbose_name= _('Local'))
    unity = models.ForeignKey(Unity,on_delete=models.CASCADE, verbose_name= _('Unidade'))

    class Meta:        
        verbose_name = 'Câmera OCR'
        verbose_name_plural = 'Câmeras OCR'

    def __str__(self):
        return self.code


class OCRCameraEvent(TimeStampedModel):    
    TYPE = [
        ( 1, _("Entrada")),
        ( 2, _("Saída")),        
    ]
    cameraOCR = models.ForeignKey(OCRCamera,on_delete=models.CASCADE, verbose_name= _('Câmera OCR'))
    event_date = models.DateTimeField(verbose_name= _('Data/Hora'))
    plate = models.CharField(max_length=7, verbose_name= _('Placa'))
    type = models.IntegerField(choices=TYPE, default=1, verbose_name=_('Tipo'))

    class Meta:        
        verbose_name = 'Câmera OCR - Evento'
        verbose_name_plural = 'Câmeras OCR - Eventos'

    def save(self, *args, **kwargs):
        """"
        um evento de entrada cria uma nova visita.
        um evento de saída, busca o ultima visita da placa e atualiza ela.
        """
        try:            
            if self.type == 1:
                visitor = Visitor()
                visitor.enter_date = self.event_date
                visitor.plate = self.plate
                visitor.status = 1 # enter
                visitor.unity = self.cameraOCR.unity
                visitor.save()
                
                restriction = Restriction.objects.filter(plate=self.plate).last()
                if not restriction is None:
                    alert = OCRCameraAlert()
                    alert.plate = self.plate
                    alert.alert_date = self.event_date
                    alert.description = restriction.description
                    alert.save()
            else:                
                visitor = Visitor.objects.filter(plate=self.plate).latest('plate')
                visitor.status = 2 # exit
                visitor.exit_date = self.event_date
                visitor.unity = self.cameraOCR.unity
                visitor.save()
                visitor.commit()
            
        except: pass
        super(OCRCameraEvent, self).save(*args, **kwargs)

    def __str__(self):
        return  '{} - {}'.format(self.cameraOCR, self.plate)
    

class SpaceAlert(TimeStampedModel):
    alert_date = models.DateTimeField(verbose_name= _('Data/Hora'))
    space = models.ForeignKey(Space,on_delete=models.CASCADE, verbose_name= _('Vaga'))
    description = models.CharField(max_length=50, verbose_name= _('Descrição'))

    class Meta:        
        verbose_name = 'Vaga - Alerta'
        verbose_name_plural = 'Vagas - Alertas'

    def __str__(self):
        return  '{} - {}'.format(self.alert_date, self.space.code)


class OCRCameraAlert(TimeStampedModel):
    alert_date = models.DateTimeField(verbose_name= _('Data/Hora'))
    plate = models.CharField(max_length=7, verbose_name= _('Placa'))
    description = models.CharField(max_length=50, verbose_name= _('Descrição'))

    class Meta:        
        verbose_name = 'Câmera OCR - Alerta'
        verbose_name_plural = 'Câmeras OCR - Alertas'

    def __str__(self):
        return  '{} - {}'.format(self.alert_date, self.plate)


class Visitor(TimeStampedModel):
    STATUS = [
        ( 1, _("Dentro")),
        ( 2, _("Fora")),        
    ]

    plate = models.CharField(max_length=7, verbose_name= _('Placa'))
    status = models.IntegerField(choices=STATUS, default=1, verbose_name=_('Situação'))
    enter_date = models.DateTimeField(verbose_name= _('Entrada'))
    exit_date = models.DateTimeField(blank=True, null=True, verbose_name= _('Saída'))
    unity = models.ForeignKey(Unity,on_delete=models.CASCADE, verbose_name= _('Unidade'))

    class Meta:        
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'

    def __str__(self):
        return  self.plate
    

class Restriction(TimeStampedModel):
    plate = models.CharField(max_length=7, verbose_name= _('Placa'))
    expiration_date = models.DateTimeField(blank=True, null=True, verbose_name= _('Data de validade'))
    description = models.CharField(max_length=50, verbose_name= _('Descrição'))
    unity = models.ForeignKey(Unity,on_delete=models.CASCADE, verbose_name= _('Unidade'))

    class Meta:        
        verbose_name = 'Restrições'
        verbose_name_plural = 'Restrições'

    def __str__(self):
        return  self.plate