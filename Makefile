train:
	/home/wav2letter/build/Train train --flagsfile aishell/train_seq2seq_tds.cfg

distrib_train:
	mpirun --allow-run-as-root -n 8 /home/wav2letter/build/Train train --flagsfile aishell/train_seq2seq_tds.cfg --enable_distributed true

test:
	/home/wav2letter/build/Test  \
	--am=seq2seq_tds_trainlogs/001_model_data#dev.bin \
	--test=data/test \
	--maxload=-1 \
	--show

decode:
	/home/wav2letter/build/Decoder --flagsfile aishell/decode_seq2seq_tds.cfg
