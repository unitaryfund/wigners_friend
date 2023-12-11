# wigners_friend

Repository for the extended Wigner's friend experiment

## Configuration

To install this project, one can run:

```
pip install -e .
```

Then, one can run the content in the `examples/` directory as, for instance:

```
python examples/run.py
```

## Running on IBM hardware

In order to run on IBM hardware, you will require an IBM account and a IBM API token. If you have an IBM Quantum
account, you can obtain the API token [here](https://quantum.ibm.com/)

You will then need to create a `.env` file in `wigners_friend/.env` where

```
IBM_PROVIDER_TOKEN="<IBM_TOKEN>"
```

where `<IBM_TOKEN>` is the token obtained from your IBM Quantum Platform account.

You will also need to set the `USE_HARDWARE = True` option in `config.py`.

## Running on Qiskit Aer simulator

Setting `USE_SIMULATOR = True` makes use of the Qiskit Aer simulator

## Running on noisy simulator

Setting `USE_NOISY_SIMULATOR = True` makes use of a noisy simulator based on a fake IBM device.