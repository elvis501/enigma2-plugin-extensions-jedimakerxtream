#!/usr/bin/python
# -*- coding: utf-8 -*-

# for localized messages     
from . import _

import owibranding

from Screens.Screen import Screen
from plugin import skin_path, cfg, autoStartTimer

from Components.Pixmap import Pixmap
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Sources.List import List
from Components.ConfigList import *
from Components.config import *
from Screens.VirtualKeyBoard import VirtualKeyBoard

from Screens.LocationBox import LocationBox
from Screens.MessageBox import MessageBox


class JediMakerXtream_Settings(ConfigListScreen, Screen):

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		
		skin = skin_path + 'jmx_settings.xml'
	
		
		self.dreamos = False
		
		try:
			from boxbranding import getImageDistro, getImageVersion, getOEVersion
		except:
			self.dreamos = True
			if owibranding.getMachineBrand() == "Dream Multimedia" or owibranding.getOEVersion() == "OE 2.2":
				skin = skin_path + 'DreamOS/jmx_settings.xml'
 
		with open(skin, 'r') as f:
			self.skin = f.read()

		self.setup_title = _('Settings')
		
		self.onChangedEntry = []
		
		self.list = []
		ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
		
		self['information'] = Label('')
		self['key_red'] = StaticText(_('Cancel'))
		self['key_green'] = StaticText(_('Save'))
		
		self['VirtualKB'].setEnabled(False)
		self['HelpWindow'] = Pixmap()
		self['VKeyIcon'] = Pixmap()
		self['HelpWindow'].hide()
		self['VKeyIcon'].hide()
		
		self['lab1'] = Label('')
		

		self['actions'] = ActionMap(["SetupActions"],
		{
		 'cancel': self.cancel,
		 'save': self.save,
		 'ok': self.ok,
				
		}, -2)
		 
		self.initConfig()
		self.createSetup()

		self.onLayoutFinish.append(self.layoutFinished)

		if self.setInfo not in self['config'].onSelectionChanged:
			self['config'].onSelectionChanged.append(self.setInfo)

		
	def layoutFinished(self):
		self.setTitle(self.setup_title)
		
	
	def initConfig(self):
		self.cfg_location = getConfigListEntry(_('playlists.txt location'), cfg.location)
		self.cfg_m3ulocation = getConfigListEntry(_('Local M3U File location'), cfg.m3ulocation)
		self.cfg_enabled = getConfigListEntry(_('Automatic live bouquet update'), cfg.enabled)
		self.cfg_wakeup =  getConfigListEntry(_('Automatic live update start time'), cfg.wakeup)
		self.cfg_main = getConfigListEntry(_('Show in main menu'), cfg.main)
		self.cfg_extensions = getConfigListEntry(_('Show in extensions'), cfg.extensions)
		self.cfg_skin = getConfigListEntry(_('Select skin'), cfg.skin)
		self.cfg_timeout = getConfigListEntry(_('Server timeout (seconds)'), cfg.timeout)
		self.cfg_catchup = getConfigListEntry(_('Prefix Catchup channels'), cfg.catchup)
		self.cfg_catchupprefix = getConfigListEntry(_('Select Catchup prefix symbol'), cfg.catchupprefix)
		self.cfg_groups = getConfigListEntry(_('Group bouquets into its own folder'), cfg.groups)
		self.cfg_placement = getConfigListEntry(_("Place Bouquet at"), cfg.placement)
		

	def createSetup(self):
		self.list = []
		self.list.append(self.cfg_location)
		self.list.append(self.cfg_m3ulocation)
		self.list.append(self.cfg_enabled)
		
		if cfg.enabled.value == True:
			self.list.append(self.cfg_wakeup)
		
		self.list.append(self.cfg_groups)
		self.list.append(self.cfg_placement)
		self.list.append(self.cfg_catchup)  
		if cfg.catchup.value == True:
			self.list.append(self.cfg_catchupprefix) 
		self.list.append(self.cfg_timeout)  
		self.list.append(self.cfg_main)
		self.list.append(self.cfg_extensions)
		self.list.append(self.cfg_skin)
		
		self['config'].list = self.list
		self['config'].l.setList(self.list)

		self.setInfo()
		self.handleInputHelpers()
		
	# dreamos workaround for showing setting descriptions
	def setInfo(self):
		
		entry = str(self.getCurrentEntry())

		if entry == _('playlists.txt location'):
			self['information'].setText(_("Select the location of your playlists.txt file. i.e. /media/hdd/playlists. Press 'OK' to change location.\n\nDefault location is /etc/enigma2/jediplaylists"))
			return
			
		if entry == _('Local M3U File location'):
			self['information'].setText(_("Select the location of your local m3u files. i.e. /media/hdd/playlists. Press 'OK' to change location.\n\nDefault location is /etc/enigma2/jediplaylists"))
			return
			
		if entry == _('Automatic live bouquet update'):
			self['information'].setText(_("Update your live bouquets automatically."))
			return
			
		if entry == _('Automatic live update start time'):
			self['information'].setText(_("Select the time of the automatic update."))
			return
			
		if entry == _('Show in main menu'):
			self['information'].setText(_("Display JediMakerXtream in Main Menu.\n*Restart GUI required."))
			return
			
		if entry == _('Show in extensions'):
			self['information'].setText(_("Quick start JediMakerXtream playlists from extensions menu.\n*Restart GUI required."))
			return
 
		if entry == _('Select skin'):
			self['information'].setText(_("Select from the available skins.\n*Restart GUI required."))
			return
			
		if entry == _('Server timeout (seconds)'):
			self['information'].setText(_("Amend the timeout on server calls.\n\nCan be increased for very large playlists, slow servers, or slow proxies."))
			return
			
		if entry == _('Prefix Catchup channels'):
			self['information'].setText(_("Mark channels that have catchup with a prefix in your bouquets."))
			return
			
		if entry == _('Select Catchup prefix symbol'):
			self['information'].setText(_("Select the symbol to prefix your catchup channels with."))
			return
			
		if entry == _('Group bouquets into its own folder'):
			self['information'].setText(_("Create a group bouquet for each playlist.\n *Experimental* "))
			return
			
		if entry == _('Place Bouquet at'):
			self['information'].setText(_("Place created IPTV bouquets at top or bottom of current bouquets."))
			return
			
		

	def handleInputHelpers(self):
		if self['config'].getCurrent() is not None:
			if isinstance(self['config'].getCurrent()[1], ConfigText) or isinstance(self['config'].getCurrent()[1], ConfigPassword) :
				if self.has_key('VKeyIcon'):
					if isinstance(self['config'].getCurrent()[1], ConfigNumber):
						self['VirtualKB'].setEnabled(False)
						self['VKeyIcon'].hide()
					else:
						self['VirtualKB'].setEnabled(True)
						self['VKeyIcon'].show()
				
				if not isinstance(self['config'].getCurrent()[1], ConfigNumber):
					
					 if isinstance(self['config'].getCurrent()[1].help_window, ConfigText) or isinstance(self['config'].getCurrent()[1].help_window, ConfigPassword):
						if self['config'].getCurrent()[1].help_window.instance is not None:
							helpwindowpos = self['HelpWindow'].getPosition()

							if helpwindowpos:
								helpwindowposx, helpwindowposy = helpwindowpos
								if helpwindowposx and helpwindowposy:
									from enigma import ePoint
									self['config'].getCurrent()[1].help_window.instance.move(ePoint(helpwindowposx,helpwindowposy))
				
			else:
				if self.has_key('VKeyIcon'):
					self['VirtualKB'].setEnabled(False)
					self['VKeyIcon'].hide()
		else:
			if self.has_key('VKeyIcon'):
				self['VirtualKB'].setEnabled(False)
				self['VKeyIcon'].hide()
					   
	
	def changedEntry(self):
		self.item = self['config'].getCurrent()
		for x in self.onChangedEntry:
			x()
			
		try:
			if isinstance(self['config'].getCurrent()[1], ConfigEnableDisable) or isinstance(self['config'].getCurrent()[1], ConfigYesNo) or isinstance(self['config'].getCurrent()[1], ConfigSelection):
				self.createSetup()
		except:
			pass


	def getCurrentEntry(self):
		return self['config'].getCurrent() and self['config'].getCurrent()[0] or ''

	def getCurrentValue(self):
		return self['config'].getCurrent() and str(self['config'].getCurrent()[1].getText()) or ''


	def save(self):
		global autoStartTimer
		
		if self['config'].isChanged():
			for x in self['config'].list:
				x[1].save()
			configfile.save()
			
		if autoStartTimer is not None:
			autoStartTimer.update()
		self.close(True)
		return
		
		
	def cancel(self, answer = None):
		if answer is None:
			if self['config'].isChanged():
				self.session.openWithCallback(self.cancel, MessageBox, _('Really close without saving settings?'))
			else:
				self.close()
		elif answer:
			for x in self['config'].list:
				x[1].cancel()
				
			self.close()
		return
	
	
	def ok(self):
		ConfigListScreen.keyOK(self)
		sel = self['config'].getCurrent()[1]
		if sel and sel == cfg.location:
			self.setting = 'playlist'
			self.openDirectoryBrowser(cfg.location.value)
		if sel and sel == cfg.m3ulocation:
			self.setting = 'm3u'
			self.openDirectoryBrowser(cfg.m3ulocation.value)
		else:
			pass


	def openDirectoryBrowser(self, path):
		try:
			self.session.openWithCallback(
			 self.openDirectoryBrowserCB,
			 LocationBox,
			 windowTitle=_('Choose Directory:'),
			 text=_('Choose directory'),
			 currDir=str(path),
			 bookmarks=config.movielist.videodirs,
			 autoAdd=False,
			 editDir=True,
			 inhibitDirs=['/bin', '/boot', '/dev', '/home', '/lib', '/proc', '/run', '/sbin', '/sys', '/var'],
			 minFree=15)
		except Exception as e:
			print("[jmxSettings] openDirectoryBrowser get failed: %s" % e)
		except:
			pass


	def openDirectoryBrowserCB(self, path):
			if path is not None:
				if self.setting == 'playlist':
					cfg.location.setValue(path)
				if self.setting == 'm3u':
					cfg.m3ulocation.setValue(path)
			return
