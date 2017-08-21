program recarray

  nrec=119
  write(1,*),nrec 

  do i=1,nrec
     
     r=0.0
     xlat=1.0+i*0.2
     xlong=xlat
     write(1,'(3f6.2)')r,xlat,xlong 
     write(1,'(a1)')'5'
     write(1,'(a10)')'1 1 1 1 1'
     write(1,'(a10)')'1 2 3 4 5'

  end do

end program recarray
