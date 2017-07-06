# Tai Sakuma <tai.sakuma@cern.ch>
import collections
import itertools

import obj

##__________________________________________________________________||
class ComponentName(object):

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__,
        )

    def begin(self, event):
        self.vals = [ ]
        event.componentName = self.vals

        self.vals[:] = [event.component.name]
        # e.g., "HTMHT_Run2015D_PromptReco_25ns"

    def event(self, event):
        event.componentName = self.vals

##__________________________________________________________________||
class SMSMass(object):
    def begin(self, event):

        massdict = {
            'SMS_T1tttt': ('GenSusyMGluino', 'GenSusyMNeutralino'),
            'SMS_T1bbbb': ('GenSusyMGluino', 'GenSusyMNeutralino'),
            'SMS_T1qqqq': ('GenSusyMGluino', 'GenSusyMNeutralino'),
            'SMS_T2tt': ('GenSusyMStop', 'GenSusyMNeutralino'),
            'SMS_T2bb': ('GenSusyMSbottom', 'GenSusyMNeutralino'),
            'SMS_T2qq': ('GenSusyMSquark', 'GenSusyMNeutralino'),
        }

        smsname =  '_'.join(event.componentName[0].split('_')[0:2])
        # e.g., 'SMS_T1tttt'

        self.sms = smsname in massdict

        if not self.sms: return

        self.mass1, self.mass2 = massdict[smsname]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        event.smsmass1 = getattr(event, self.mass1)
        event.smsmass2 = getattr(event, self.mass2)

    def event(self, event):
        if not self.sms: return
        self._attach_to_event(event)

##__________________________________________________________________||
class ArraysIntoObjectZip(object):
    """zip a set of arrays into a list of objects

    """

    def __init__(self,
                 in_array_prefix, in_array_names,
                 out_obj = None, out_attr_names = None):

        self.in_array_prefix = in_array_prefix
        # e.g., 'jet'

        self.in_array_names = in_array_names
        # e.g., ['pt', 'eta', 'phi']

        self.out_obj = out_obj if out_obj else in_array_prefix
        # e.g., 'Jet'

        self.out_attr_names = out_attr_names if out_attr_names else in_array_names
        # e.g., ['Pt', 'Eta', 'Phi']

        if not len(self.in_array_names) == len(self.out_attr_names):
            raise ValueError('in_array_names and out_attr_names must have the same length: in_array_names = {}, out_attr_names = {}'.format(in_array_names, out_attr_names))

        self.in_names = ['{}_{}'.format(in_array_prefix, v) for v in in_array_names]
        # e.g., ['jet_pt', 'jet_eta', 'jet_phi']

    def __repr__(self):
        name_value_pairs = (
            ('in_array_prefix', self.in_array_prefix),
            ('in_array_names',  self.in_array_names),
            ('out_obj',         self.out_obj),
            ('out_attr_names',  self.out_attr_names),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self, event):
        self.out = [ ]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        setattr(event, self.out_obj, self.out)
        # e.g., event.Jet = [ ]

    def event(self, event):
        self._attach_to_event(event)

        arrays = (getattr(event, n) for n in self.in_names)
        # e.g., (event.jet_pt, event.jet_eta, event.jet_phi)

        attr_values_list = itertools.izip(*arrays)
        # e.g., ((pt[0], eta[0], phi[0]), (pt[1], eta[1], phi[1]), ...)

        attr_name_value_pairs = (zip(self.out_attr_names, attr_values) for attr_values in attr_values_list)
        # e.g., ((('Pt', (pt[0]), ('Eta', eta[0]), ('Phi', phi[0])),
        #        (('Pt', (pt[1]), ('Eta', eta[1]), ('Phi', phi[1])), ...)
        # print attr_name_value_pairs

        self.out[:] = [obj.Object(pair) for pair in attr_name_value_pairs]
        # e.g., [Object(), Object(), ...]

    def end(self):
        self.out = None

##__________________________________________________________________||
