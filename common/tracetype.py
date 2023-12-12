import numpy as np
import pandas as pd
from pandas.api.extensions import ExtensionScalarOpsMixin
from pandas.core.arrays import ExtensionArray
from pandas.core.dtypes.base import ExtensionDtype


class Trace:
    def __init__(self, val, meta=None, orig=None):
        # print(orig)
        if meta is None:
            meta = set()
        if isinstance(meta, Trace):
            meta = Trace.meta
        if not isinstance(meta, set):
            meta = {meta}
        if isinstance(val, Trace):
            meta = meta | val.meta
            val = val.val
        if meta == set() and orig is not None:
            if isinstance(orig, Trace):
                orig = Trace.meta
            if not isinstance(orig, set):
                orig = {orig}
            meta = orig

        self.val = val
        self.meta = meta

    def is_nan(self):
        return pd.isnull(self.val)

    # def isna(self):
    #    return pd.isnull(self.val)

    def __hash__(self):
        return hash(self.val)

    # https://diveintopython3.net/special-method-names.html

    def __str__(self):
        return str(self.val) + "`"
        # return str(self.val) + "_" + str(self.meta)
        # return repr(self)

    def __repr__(self):
        return "Trace(" + repr(self.val) + ', ' + repr(self.meta) + ')'

    def __add__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val + other.val, self.meta | other.meta)

    def __sub__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val - other.val, self.meta | other.meta)

    def __mul__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val * other.val, self.meta | other.meta)

    def __truediv__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val / other.val, self.meta | other.meta)

    def __floordiv__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val // other.val, self.meta | other.meta)

    def __mod__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val % other.val, self.meta | other.meta)

    # skip divmod for now

    def __pow__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val ** other.val, self.meta | other.meta)

    def __lshift__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val << other.val, self.meta | other.meta)

    def __rshift__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val >> other.val, self.meta | other.meta)

    def __and__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val & other.val, self.meta | other.meta)

    def __xor__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val ^ other.val, self.meta | other.meta)

    def __or__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val | other.val, self.meta | other.meta)

    # r

    def __radd__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(other.val + self.val, self.meta | other.meta)

    def __rsub__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(other.val - self.val, self.meta | other.meta)

    def __rmul__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(other.val * self.val, self.meta | other.meta)

    def __rtruediv__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(other.val / self.val, self.meta | other.meta)

    def __rfloordiv__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(other.val // self.val, self.meta | other.meta)

    def __rmod__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(other.val % self.val, self.meta | other.meta)

    # skip rdivmod for now

    def __rpow__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(other.val ** self.val, self.meta | other.meta)

    def __rlshift__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(other.val << self.val, self.meta | other.meta)

    def __rrshift__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(other.val >> self.val, self.meta | other.meta)

    def __rand__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(other.val & self.val, self.meta | other.meta)

    def __rxor__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(other.val ^ self.val, self.meta | other.meta)

    def __ror__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(other.val | self.val, self.meta | other.meta)

    # unary

    def __neg__(self):
        return Trace(-self.val, self.meta)

    def __pos__(self):
        return Trace(+self.val, self.meta)

    def __abs__(self):
        return Trace(abs(self.val), self.meta)

    def __invert__(self):
        return Trace(~self.val, self.meta)

    def __complex__(self):
        return Trace(complex(self.val), self.meta)

    def __int__(self):
        return Trace(int(self.val), self.meta)

    def __float__(self):
        return Trace(float(self.val), self.meta)

    def __round__(self):
        return Trace(round(self.val), self.meta)

    def __round__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(round(self.val, other.val), self.meta | other.meta)

    def __ceil__(self):
        return Trace(math.ceil(self.val), self.meta)

    def __floor__(self):
        return Trace(math.floor(self.val), self.meta)

    def __trunc__(self):
        return Trace(math.trunc(self.val), self.meta)

    def __index__(self):
        return self.val.__int__()

    # comp

    def __eq__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(True, self.meta | other.meta)
        if self.is_nan():
            return Trace(False, self.meta)
        if other.is_nan():
            return Trace(False, other.meta)
        return Trace(self.val == other.val, self.meta | other.meta)

    def __ne__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(False, self.meta | other.meta)
        if self.is_nan():
            return Trace(True, self.meta)
        if other.is_nan():
            return Trace(True, other.meta)
        return Trace(self.val != other.val, self.meta | other.meta)

    def __lt__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val < other.val, self.meta | other.meta)

    def __le__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val <= other.val, self.meta | other.meta)

    def __gt__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val > other.val, self.meta | other.meta)

    def __ge__(self, other):
        if not isinstance(other, Trace):
            other = Trace(other)
        if self.is_nan() and other.is_nan():
            return Trace(pd.NA, self.meta | other.meta)
        if self.is_nan():
            return self
        if other.is_nan():
            return other
        return Trace(self.val >= other.val, self.meta | other.meta)

    def __bool__(self):
        return self.val.__bool__()

    def __call__(self, *args, **kwargs):
        return self.val(*args, **kwargs)


class TraceDtype(ExtensionDtype):
    """A custom data type, to be paired with an ExtensionArray."""

    type = Trace
    name = "Trace"
    na_value = pd.NA

    def __init__(self, orig=None):
        self.orig = orig
        #self.na_value = Trace(pd.NA, orig)

    @classmethod
    def construct_array_type(cls):
        """Return the array type associated with this dtype."""
        return TraceArray


class TraceArray(ExtensionArray, ExtensionScalarOpsMixin):
    """Abstract base class for custom 1-D array types."""

    def __init__(self, values, orig=None, dtype=None, copy=False):
        """Instantiate the array.
        If you're doing any type coercion in here, you will also need
        that in an overwritten __setitem__ method.
        But, here we coerce the input values into Decimals.
        """
        if isinstance(dtype, TraceDtype) and orig is None:
            orig = dtype.orig
        values = [Trace(val, None, orig) for val in values]
        self._data = np.asarray(values, dtype=object)
        self._dtype = TraceDtype(orig)

    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        """Construct a new ExtensionArray from a sequence of scalars."""
        return cls(scalars, dtype=dtype)

    @classmethod
    def _from_factorized(cls, values, original):
        """Reconstruct an ExtensionArray after factorization."""
        return cls(values)

    def __getitem__(self, item):
        """Select a subset of self."""
        return self._data[item]

    def __len__(self) -> int:
        """Length of this array."""
        return len(self._data)

    @property
    def nbytes(self):
        """The byte size of the data."""
        return self._itemsize * len(self)

    @property
    def dtype(self):
        """An instance of 'ExtensionDtype'."""
        return self._dtype

    def isna(self):
        """A 1-D array indicating if each value is missing."""
        return np.array([x.is_nan() for x in self._data], dtype=bool)

    def take(self, indexer, allow_fill=False, fill_value=None):
        """Take elements from an array.
        Relies on the take method defined in pandas:
        https://github.com/pandas-dev/pandas/blob/e246c3b05924ac1fe083565a765ce847fcad3d91/pandas/core/algorithms.py#L1483
        """
        from pandas.api.extensions import take

        data = self._data
        if allow_fill and fill_value is None:
            fill_value = self.dtype.na_value

        result = take(
            data, indexer, fill_value=fill_value, allow_fill=allow_fill)
        return self._from_sequence(result)

    def copy(self):
        """Return a copy of the array."""
        return type(self)(self._data.copy())

    @classmethod
    def _concat_same_type(cls, to_concat):
        """Concatenate multiple arrays."""
        return cls(np.concatenate([x._data for x in to_concat]))

# https://pandas.pydata.org/docs/development/extending.html#:~:text=pandas%20itself%20uses%20the%20extension,custom%20array%20and%20data%20type


TraceArray._add_arithmetic_ops()
TraceArray._add_comparison_ops()


def trace(df, orig=None):
    return df.astype('O').astype(TraceDtype(orig)).astype('O')


def isna(df):
    return df.astype(TraceDtype()).isna()


def dropna(df, axis=0):
    return df.astype(TraceDtype()).dropna(axis=axis).astype('O')


def untrace(data):
    if isinstance(data, list):
        return [x.val for x in data]
    if isinstance(data, pd.DataFrame):
        return trace(data,None).applymap(lambda x: x.val)
    try:
        return data.val
    except:
        return data


def gettrace(data):
    if isinstance(data, list):
        return [x.meta for x in data]
    if isinstance(data, pd.DataFrame):
        return trace(data,None).applymap(lambda x: x.meta)
    try:
        return data.meta
    except:
        return data